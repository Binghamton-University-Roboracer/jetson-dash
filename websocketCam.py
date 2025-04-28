import numpy as np
import websockets
import cv2
import base64

import asyncio


async def videoStream(websocket):
    cap = cv2.VideoCapture(4)
    if not cap.isOpened():
        print("Error: Could not open video");
        return 
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            edges = cv2.Canny(gray, 50, 150)

            lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=100, minLineLength=50, maxLineGap=10)
       	    if lines is not None:
                for line in lines:
                    x1, y1, x2, y2 = line[0]
                    cv2.line(gray, (x1, y1), (x2, y2), (0, 255, 0), 2)
            _, buffer = cv2.imencode('.jpg', gray)
            jpg_as_text = base64.b64encode(buffer).decode('utf-8')
            
            await websocket.send(jpg_as_text)
            await asyncio.sleep(0.066)  # ~30 FPS
    except websockets.exceptions.ConnectionClosed:
        print("Client disconnected. Stopping video stream.")
    finally:
        cap.release()  # Release the camera when the client disconnects
        
async def main():
    async with websockets.serve(videoStream, "0.0.0.0", 8080):
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())
