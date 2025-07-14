from PIL import Image
import numpy as np
import base64
import json
import os

def handler(request):
    if request.method != "POST":
        return {
            "statusCode": 405,
            "body": json.dumps({"error": "Only POST allowed"})
        }

    try:
        body = request.json()
        image_data = body.get("image_base64")

        if not image_data:
            return {"statusCode": 400, "body": json.dumps({"error": "No image_base64 provided"})}

        # Decode image
        image_bytes = base64.b64decode(image_data)
        img = Image.open(io.BytesIO(image_bytes)).convert("L")  # grayscale
        width, height = img.size

        # Split image into 5 parts
        parts = [img.crop((i * width // 5, 0, (i + 1) * width // 5, height)).resize((64, 64)) for i in range(5)]
        vectors = [np.array(p).flatten() for p in parts]

        # Compare each vector to others using Euclidean distance
        scores = []
        for i in range(5):
            others = [vectors[j] for j in range(5) if j != i]
            dist = [np.linalg.norm(vectors[i] - o) for o in others]
            avg_dist = sum(dist) / len(dist)
            scores.append(avg_dist)

        paling_beda = int(np.argmax(scores)) + 1
        return {
            "statusCode": 200,
            "body": json.dumps({"paling_beda": paling_beda})
        }

    except Exception as e:
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}
      
