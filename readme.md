# Semi-Automatic Grading GUI with GPT-4o Mini

## Description

This project provides a graphical user interface (GUI) for semi-automatic grading of short student answers using GPT-4o Mini via the OpenAI API. It follows a human-in-the-loop workflow: the user manually grades a small set of answers, then leverages a Retrieval-Augmented Generation (RAG) system to evaluate the rest based on a customizable prompt.

## Features

- Load Excel files containing student responses.
- Clean text on import using optional preprocessing tools.
- Manually assign scores to a subset of answers.
- Evaluate model performance by comparing AI vs human scores.
- Edit the prompt used by the LLM directly via `prompt.txt`.
- Automatically grade remaining responses using GPT-4o Mini.
- Visualize confidence and coverage tradeoffs.
- Export results with separate columns for human and AI scores.

---

## How to Use

1. **Load the Excel File**  
   Launch the application and select the Excel file to process. Optionally, enable text-cleaning options before loading.

2. **Manual Grading**  
   In the main table, assign scores to a representative set of student responses, including both correct and incorrect examples. You can also pre-grade these in Excel before opening the interface.

3. **Apply Corrections**  
   Click the **Apply Corrections** button to store your manual grades in the appropriate Excel column.

4. **Test the Model**  
   Press **Test** to compare the AI-generated grades with your manual scores. Review discrepancies and inspect the model’s feedback to understand its decisions.

5. **Refine the Prompt**  
   If needed, open `prompt.txt` in the project directory to modify the grading instructions used by the model. The changes will be applied automatically during the next test.

6. **Iterate**  
   Continue testing and refining the prompt until the AI’s behavior matches your grading expectations.

7. **AI Grading**  
   Click **AI Correction** to evaluate all remaining, ungraded responses. This step uses GPT-4o Mini via OpenAI’s API and may take a few minutes depending on dataset size.

8. **Review Results and Confidence**  
   Once completed, the system adds new columns to the table:
   - `AI Score`
   - `Feedback`
   - `Confidence`  
   A threshold analysis panel also appears, showing performance tradeoffs at different confidence levels.

9. **Save Results**  
   Choose a confidence threshold and click **Close and Save**. The final Excel file will be saved in the `outputs/` folder. Both human and AI scores are preserved in separate columns for clarity.

**For more information check Section 6 in TFM_Cheriha_Mounir.pdf**
---

## Setup and Installation

1. **Clone the Repository**

```bash
git clone https://github.com/MounirCheriha/semi-auto-grading-gui.git
cd semi-auto-grading-gui
```

2. **Install Dependencies**

```bash
pip install -r requirements.txt
```

3. **Add Your OpenAI API Key**

Create a file called api_key.txt in the root directory and paste your OpenAI API key inside.

⚠️ Keep this file private — do not share your API key.

## File Structure

The project is organized into the following main components:

📁 semi-auto-grading-gui/
├── main.py # Entry point that launches the graphical user interface
├── prompt.txt # Editable prompt used for guiding the LLM during grading
├── api_key.txt # Stores your OpenAI API key. Warning: Do not upload this file to public repositories.
├── requirements.txt # Python dependencies required to run the project
├── outputs/ # Directory where corrected Excel files are saved
├── core/ # Scripts related to grading logic and LLM integration
├── gui/ # Scripts that handle GUI components and interactions
└── assets/ # UI layout files (.ui) used by the interface

## License

## Author 

Mounir Cheriha Dkik