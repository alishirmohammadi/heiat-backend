#!/usr/bin/env bash
python3 manage.py migrate
python3 manage.py convert_birth_date
python3 manage.py convert_mugshot_to_image
python3 manage.py convert_note_to_posts
python3 manage.py convert_pricing_to_shift
python3 manage.py convert_state
python3 manage.py convert_additional_option_to_qa
python3 manage.py convert_message
python3 manage.py convert_feedback_to_message
