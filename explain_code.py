import os
import sys
import openai


if len(sys.argv) == 2:
    openai.api_key = os.getenv("OPENAI_API_KEY")
    file_path = sys.argv[1]
    
    try:
        with open(file_path) as fp:
            code = fp.read()
        prompt = f"""
            # Python 3
            
            {code}
            
            # Explanation of what the code does\n\n#
        """
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            temperature=0,
            max_tokens=150,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )
        
        print(response["choices"][0]['text'])
    except Exception as e:
        print("unable to process file", e)