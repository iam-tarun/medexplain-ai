import gradio as gr

def testing(test_name, value):
  return (
    f"your test name is {test_name}\n"
    f"you results are {value}"
  )

with gr.Blocks() as app:
  gr.Markdown("MedExplain AI")
  gr.Markdown("Enter a lab test result to get a simple explanation")

  with gr.Row():
    test_input = gr.Textbox(label="Test Name", placeholder="e.g., Vitamin D")
    value_input = gr.Textbox(label="Value", placeholder="e.g, 12mg/mL")
  
  output = gr.Textbox(label="Explanation")

  submit_btn = gr.Button("Explain")
  submit_btn.click(fn=testing, inputs=[test_input, value_input], outputs=output)



if __name__ == "__main__":
  app.launch()