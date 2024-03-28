import openai
from dotenv import find_dotenv, load_dotenv
import time
import logging
from datetime import datetime

load_dotenv()
# openai.api_key = os.environ.get("OPENAI_API_KEY")
# defaults to getting the key using os.environ.get("OPENAI_API_KEY")
# if you saved the key under a different environment variable name, you can do something like:
# client = OpenAI(
#   api_key=os.environ.get("CUSTOM_ENV_NAME"),
# )

client = openai.OpenAI()
model = "gpt-3.5-turbo-16k"

# ==  Create our Assistant (Uncomment this to create your assistant) ==

#personal_business_coach = client.beta.assistants.create(
#   name="Healthcare UX Consultancy Coach",
#   instructions="""You are a seasoned business coach with deep expertise in the UX consultancy realm, specifically tailored to the healthcare sector. You possess comprehensive knowledge on establishing and growing a UX consultancy, including market analysis, service development, regulatory compliance, branding, client acquisition strategies, and operational challenges specific to healthcare. You understand the importance of user-centered design in improving patient care and are familiar with healthcare regulations like HIPAA and relevant Norwegian laws. Your guidance is practical, aiming to help navigate the complexities of the healthcare industry effectively.""",
#   model=model 
#)
#
#asistant_id = personal_business_coach.id
#print(asistant_id)


# === Thread (uncomment this to create your Thread) ===
#thread = client.beta.threads.create(
#    messages=[
#        {"role": "user",
#         "content": "I'm in the early stages of planning my UX consultancy focused on the healthcare sector. Given the critical nature of healthcare systems and the stringent regulations like HIPAA, what should be my initial steps in conducting a comprehensive market analysis? Specifically, I'm interested in identifying pressing needs within digital health products that my consultancy could address. Additionally, how should I approach the development of UX services that not only meet regulatory compliance but also significantly improve user experience for both medical professionals and patients?"}
#    ]
#)

#Thread ID
#thread_id = thread.id
#print(thread_id)

# === Hardcode our ids ==
asistant_id = "asst_i9WFAMOM18QGXZ9nilszbHbl"
thread_id = "thread_n5WeAVscH8ofChxqUgLMZqs2"

# ==== Create a Message ====
message = "Please suggest a breakdown of prospects and how to address them?"
message = client.beta.threads.messages.create(
    thread_id=thread_id, role="user", content=message
)

# === Run our Assistant ===
run = client.beta.threads.runs.create(
    thread_id=thread_id,
    assistant_id=asistant_id,
    instructions="Please address the user as Norendal, Torstein Norendal",
)

def wait_for_run_completion(client, thread_id, run_id, sleep_interval=5):
    """

    Waits for a run to complete and prints the elapsed time.:param client: The OpenAI client object.
    :param thread_id: The ID of the thread.
    :param run_id: The ID of the run.
    :param sleep_interval: Time in seconds to wait between checks.
    """
    while True:
        try:
            run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)
            if run.completed_at:
                elapsed_time = run.completed_at - run.created_at
                formatted_elapsed_time = time.strftime(
                    "%H:%M:%S", time.gmtime(elapsed_time)
                )
                print(f"Run completed in {formatted_elapsed_time}")
                logging.info(f"Run completed in {formatted_elapsed_time}")
                # Get messages here once Run is completed!
                messages = client.beta.threads.messages.list(thread_id=thread_id)
                last_message = messages.data[0]
                response = last_message.content[0].text.value
                print(f"Assistant Response: {response}")
                break
        except Exception as e:
            logging.error(f"An error occurred while retrieving the run: {e}")
            break
        logging.info("Waiting for run to complete...")
        time.sleep(sleep_interval)


# === Run ===
wait_for_run_completion(client=client, thread_id=thread_id, run_id=run.id)

# ==== Steps --- Logs ==
run_steps = client.beta.threads.runs.steps.list(thread_id=thread_id, run_id=run.id)
print(f"Steps---> {run_steps.data[0]}")