import gradio as gr
import requests
import base64

API_URL = "http://localhost:8000"

def process_audio(email, audio, summary_type, solution_types):
    if not email:
        return "Please enter your email.", "", "", {}, ""
    if not audio:
        return "Please upload an audio file.", "", "", {}, ""
    
    # Convert audio file to base64
    with open(audio, "rb") as audio_file:
        audio_bytes = audio_file.read()
    audio_base64 = base64.b64encode(audio_bytes).decode('utf-8')
    
    # Transcribe audio
    try:
        transcribe_response = requests.post(
            f"{API_URL}/transcribe",
            json={"email": email, "audio_file": audio_base64}
        ).json()
        transcription = transcribe_response['transcription']
    except Exception as e:
        return f"Transcription failed: {str(e)}", "", "", {}, ""
    
    # Summarize transcription
    try:
        summarize_response = requests.post(
            f"{API_URL}/summarize",
            json={
                "email": email,
                "transcription_text": transcription,
                "summary_type": summary_type,
                "solution_types": solution_types
            }
        ).json()
        summary = summarize_response['summary']
        solutions = summarize_response['solutions']
    except Exception as e:
        return f"Summarization failed: {str(e)}", transcription, "", {}, ""
    
    return "", transcription, summary, solutions, ""

def save_options(email, transcription, summary, save_full_text, save_summary, template_text):
    try:
        requests.post(f"{API_URL}/save", json={
            "email": email,
            "full_text": transcription if save_full_text else None,
            "summary": summary if save_summary else None,
            "template": template_text if template_text else None
        })
        return "Data saved successfully."
    except Exception as e:
        return f"Failed to save data: {str(e)}"

def retrieve_data(email):
    try:
        response = requests.get(f"{API_URL}/retrieve", params={"email": email}).json()
        return response.get('full_text', ""), response.get('summary', ""), response.get('template', "")
    except Exception as e:
        return "", "", ""

# Gradio Interface
with gr.Blocks() as demo:
    gr.Markdown("# Medical Transcription and Summarization Tool")
    
    with gr.Tab("Process Audio"):
        email = gr.Textbox(label="Email")
        
        # Update type to 'filepath' since it expects a file path
        audio_input = gr.Audio(type="filepath", label="Upload Audio File")
        
        summary_type = gr.Radio(
            label="Select Summary Type",
            choices=["Brief Summary", "Detailed Summary", "Action Items"],
            value="Brief Summary"
        )
        
        solution_types = gr.CheckboxGroup(
            label="Select Solution Types",
            choices=["Medication Suggestions", "Lifestyle Advice", "Referral Suggestions"]
        )
        
        process_button = gr.Button("Process Audio")
        error_msg = gr.Textbox(label="Status", interactive=False)
        transcription = gr.Textbox(label="Transcription", lines=10)
        summary = gr.Textbox(label="Summary", lines=5)
        solutions = gr.JSON(label="AI Solutions")
        save_full_text = gr.Checkbox(label="Save Full Text")
        save_summary = gr.Checkbox(label="Save Summary")
        template_text = gr.Textbox(label="Template", lines=5)
        save_button = gr.Button("Save Options")
        
        process_button.click(
            process_audio,
            inputs=[email, audio_input, summary_type, solution_types],
            outputs=[error_msg, transcription, summary, solutions, template_text]
        )
        
        save_button.click(
            save_options,
            inputs=[email, transcription, summary, save_full_text, save_summary, template_text],
            outputs=error_msg
        )
    
    with gr.Tab("Retrieve Data"):
        email_retrieve = gr.Textbox(label="Email")
        retrieve_button = gr.Button("Retrieve Saved Data")
        retrieved_full_text = gr.Textbox(label="Saved Full Text", lines=10)
        retrieved_summary = gr.Textbox(label="Saved Summary", lines=5)
        retrieved_template = gr.Textbox(label="Saved Template", lines=5)
        
        retrieve_button.click(
            retrieve_data,
            inputs=email_retrieve,
            outputs=[retrieved_full_text, retrieved_summary, retrieved_template]
        )

demo.launch(share=True)
