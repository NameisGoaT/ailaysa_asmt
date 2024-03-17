from celery import shared_task


@shared_task
def words_in_file(file_path):
    try:
        with open(file_path, 'r') as file:
            content = file.read()
            word_count = len(content.split())
            print("wc", word_count)
            return word_count
    except FileNotFoundError:
        return "File not found"

