import websockets
import cv2
import base64

import asyncio


async def videoStream(websocket):
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open video");
        return 
    try: 
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            _, buffer = cv2.imencode('.jpg', frame)
            jpg_as_text = base64.b64encode(buffer).decode('utf-8')
            
            await websocket.send(jpg_as_text)
            await asyncio.sleep(0.033)  # ~30 FPS
    except websockets.exceptions.ConnectionClosed:
        print("Client disconnected. Stopping video stream.")
    finally:
        cap.release()  # Release the camera when the client disconnects
        
async def main():
    async with websockets.serve(videoStream, "0.0.0.0", 8080):
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())