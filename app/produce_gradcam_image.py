import base64
from PIL import Image
import io
from pytorch_grad_cam import GradCAM  
from pytorch_grad_cam.utils.image import show_cam_on_image

def reshape_transform(tensor, height=7, width=7):
    # tensor shape: [batch, 49, channels] -> [batch, 7, 7, channels]
    result = tensor.reshape(tensor.size(0), height, width, tensor.size(2))
    # [batch, 7, 7, channels] -> [batch, channels, 7, 7]
    result = result.permute(0, 3, 1, 2)
    return result

def produce_gradcam(
    model,
    image,
):
    if(False): #placeholder
        # After model prediction, before response:
        # Select the target layer for Swin Transformer (usually the last norm layer)
        target_layer = model.norm if hasattr(model, "norm") else list(model.children())[-1]
        cam = GradCAM(model=model, target_layers=[target_layer], use_cuda=False)
        grayscale_cam = cam(input_tensor=image, targets=None)[0]

        # Unnormalize image for visualization
        rgb_image = image.squeeze(0).permute(1, 2, 0).numpy()
        rgb_image = (rgb_image * [0.229, 0.224, 0.225]) + [0.485, 0.456, 0.406]
        rgb_image = rgb_image.clip(0, 1)

        cam_image = show_cam_on_image(rgb_image, grayscale_cam, use_rgb=True)

        # Convert to PNG bytes
        cam_pil = Image.fromarray(cam_image)
        buf = io.BytesIO()
        cam_pil.save(buf, format='PNG')
        cam_bytes = buf.getvalue()
        cam_base64 = base64.b64encode(cam_bytes).decode('utf-8')


    # Create a simple placeholder image (e.g., gray square)
    img = Image.new("RGB", (384, 384), color=(200, 200, 200))
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    img_bytes = buf.getvalue()
    cam_base64 = base64.b64encode(img_bytes).decode('utf-8')
    return cam_base64