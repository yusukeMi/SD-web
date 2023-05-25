from flask import Flask,render_template,request
from misc.diffusion_client import DiffusionClient
import io
import base64
from PIL import Image

dc = DiffusionClient()

############# 設定 #####################
model = "trinart_stable_diffusion_v2(115k\u30C7\u30D5\u30A9\u30EB\u30C8)" #@param ["trinart_stable_diffusion_v2(115kデフォルト)", "trinart_stable_diffusion_v2(95k)","trinart_stable_diffusion_v2(60k)",  "stable-diffusion-v-1-4-original", "waifu-diffusion(1.2)", "waifu-diffuision(1.3)","yuk/fuyuko-waifu-diffusion"]
HUGGING_FACE_TOKEN = "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" #@param {type:"string"}
NSFW_OK = True #@param {type:"boolean"}
LESS_MEMORY=True #@param {type:"boolean"}
model_deta_sets = {
    "trinart_stable_diffusion_v2(115kデフォルト)" : {
        "url": "https://huggingface.co/naclbit/trinar...",
        "file_name": "trinart2_step115000.ckpt",
        "library": "naclbit/trinart_stable_diffusion_v2",
        "revision":"diffusers-115k",
        }
        }

dc.less_memory = LESS_MEMORY
dc.hugging_face_token = HUGGING_FACE_TOKEN
dc.nsfw_ok = NSFW_OK
dc.setModel(
    model_deta_sets[model]["library"],
    model_deta_sets[model]["revision"],
    )


########### テスト #####################
dc.text2img("path/to/model", 1,512, 512, 'dog')



app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def main_page():
    if request.method == 'GET':
        # 一時的に真っ白な画像を出力画面に表示
        image = Image.new('RGB', (512, 512), color='white')
        return render_template("page.html",encoded_image=image)
    elif request.method == 'POST':
        # インプットテキストで画像生成
        input_text = request.form["prompt"]
        dc.text2img("path/to/model", 1,512, 512, input_text)
        image = dc.showResults(1)
        # 画像をバイナリストリームに変換
        image_stream = io.BytesIO()
        image.save(image_stream, format='JPEG')
        image_stream.seek(0)

        # Base64エンコード
        encoded_image = base64.b64encode(image_stream.read()).decode('utf-8')
        return render_template("page.html",encoded_image=encoded_image)

## 実行
if __name__ == "__main__":
    app.run()
