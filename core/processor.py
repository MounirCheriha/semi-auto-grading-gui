from core.embedding import build_index, retrieve_examples
from core.grader import grade
import pandas as pd
from tqdm import tqdm
import re

def leer_prompts(path_txt: str) -> tuple[str, str]:
    """
    Read and extract system and user prompts from a text file.

    Args:
        path_txt: Path to the text file containing prompts.
                  File must contain 'SYSTEM PROMPT:' and 'USER PROMPT:' sections.

    Returns:
        tuple: (system_prompt, user_prompt) extracted from the file

    Raises:
        ValueError: If the required sections are not found in the file.
    """
    with open(path_txt, 'r', encoding='utf-8') as f:
        contenido = f.read()

    # Extract SYSTEM PROMPT section
    system_match = re.search(r'SYSTEM PROMPT:\s*(.*?)\s*USER PROMPT:', contenido, re.DOTALL)
    
    # Extract USER PROMPT section
    user_match = re.search(r'USER PROMPT:\s*(.*)', contenido, re.DOTALL)

    if not system_match or not user_match:
        raise ValueError("El archivo debe contener las secciones 'SYSTEM PROMPT:' y 'USER PROMPT:'")

    system_prompt = system_match.group(1).strip()
    user_prompt = user_match.group(1).strip()

    return system_prompt, user_prompt

def evaluate_dataframe(df: pd.DataFrame, test: bool = False) -> pd.DataFrame:
    """
    Evaluate student responses using semantic similarity and AI grading.

    Args:
        df: DataFrame containing student responses and grades.
             Must contain columns: 'Respuesta', 'Nota'
        test: If True, uses half of graded examples for testing purposes.

    Returns:
        DataFrame with added columns: 'nota IA', 'feedback IA', 'confidence'

    Raises:
        ValueError: If no graded examples are available for building the index.
    """
    
    df = df.copy()
    df['Nota'] = pd.to_numeric(df['Nota'], errors='coerce')

    # Load prompts fromf ile
    txt_path = "prompt.txt"
    system_prompt, user_prompt_template = leer_prompts(txt_path)

    # Split data into base (graded) and to_evaluate (ungraded) sets
    if test==False:
        base = df[df['Nota'].notna()]        # Use all graded examples  
        to_evaluate = df[df['Nota'].isna()]  # Evaluate ungraded examples
    else:
        # For testing: use 50% of correct and incorrect examples as base
        correctas = df[df['Nota'] == 1]
        incorrectas = df[df['Nota'] == 1]

        base_correctas = correctas.sample(frac=0.5, random_state=42)
        base_incorrectas = incorrectas.sample(frac=0.5, random_state=42)

        base = pd.concat([base_correctas, base_incorrectas])
        to_evaluate = df.drop(base.index)

    if base.empty:
        raise ValueError("No hay ejemplos previamente valorados para construir el índice.")

    # Prepare data for index building
    base_respuestas = base['Respuesta'].tolist()
    base_labels = base['Nota'].astype(int).tolist()

    # Build semantic search window
    index, _, idx_map = build_index(base_respuestas, base_labels)

    # Evaluate new responses with progress bar
    for idx, row in tqdm(to_evaluate.iterrows(), total=len(to_evaluate), desc="Evaluando nuevas respuestas"):
        # Retrieve similar examples
        correct_ex, incorrect_ex = retrieve_examples(
            index, idx_map, row['Respuesta']
        )

        # Format user prompt with examples and curent answer
        user_prompt = user_prompt_template.format(
            examples_correct="\n".join(correct_ex[:3]),
            examples_incorrect="\n".join(incorrect_ex[:3]),
            student_answer=row['Respuesta']
        )

        # Get AI evaluation
        nota, feedback, confidence = grade(
            system_prompt=system_prompt,
            user_prompt=user_prompt
        )

        # Store results
        df.at[idx, 'nota IA'] = nota
        df.at[idx, 'feedback IA'] = feedback
        df.at[idx, 'confidence'] = confidence

    return df