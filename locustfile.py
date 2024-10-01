import os
import random
from locust import HttpUser, TaskSet, task, between

class UserBehavior(TaskSet):

    def get_random_image(self):
        images_folder = 'test_img'
        image_files = [f for f in os.listdir(images_folder) if f.endswith(('jpg', 'jpeg', 'png'))]
        if not image_files:
            raise ValueError("No images found in the 'test_img' directory.")
        
        selected_image = random.choice(image_files)
        return os.path.join(images_folder, selected_image)

    @task(1)
    def upload_image(self):
        image_path = self.get_random_image()
        with open(image_path, 'rb') as f:
            response = self.client.post("/upload", files={"image": f})
            print(f"Uploaded {image_path}: {response.status_code}")

    @task(1)
    def process_image(self):
        actions = ['grayscale', 'rotate']
        selected_action = random.choice(actions)
        
        # Assuming you want to process the last uploaded image (you might want to store the image ID after upload)
        image_id = 1  # Replace with appropriate logic to get the last uploaded image ID
        value = 90  # This could represent degrees for rotation
        
        response = self.client.post(f"/process/{image_id}", data={"action": selected_action, "value": value})
        print(f"Processed image ID {image_id} with action '{selected_action}': {response.status_code}")

class WebsiteUser(HttpUser):
    host = "http://127.0.0.1:5000"  # Set your Flask app's base URL here
    tasks = [UserBehavior]
    wait_time = between(1, 5)  # Adjust wait time between tasks