import ollama
import sys_msgs


assistant_convo=[sys_msgs.assistant_msg]

def search_or_not():
    sys_msg = sys_msgs.search_or_not_msg

    respons = ollama.chat(
        model='llama3.2:latest',
        messages=[{'role':'system','content':sys_msg}, assistant_convo[-1]]
    )

    content = response['message']['content']
    print(f'SEARCH OR NOT RESULTS: {content}')

    if 'true' in content.lower():
        return True
    else:
        return False

def stream_assistant_response():
    global assistant_convo
    response_stream= ollama.chat(model='llama3.2:latest', messages=assistant_convo,stream=True)
    complete_response=''
    print('AGENT:')

    for chunk in response_stream:
        print(chunk['message']['content'], end='', flush=True)
        complete_response += chunk['message']['content']
    
    assistant_convo.append({'role':'assistant','content':complete_response})
    print('\n\n')

def main():
    global assistant_convo
    
    while True:
        prompt = input('USER: \n')
        assistant_convo.append({'role': 'user', 'content':prompt})

        if search_or_not():
            print('WEB SEARCH REQUIRED')

        stream_assistant_response()

if __name__ == '__main__':
    main()


