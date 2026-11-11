from PIL import Image
import os, glob

imgs = [
    r"C:/Users/hp/.gemini/antigravity/brain/f58d96fb-8903-4428-b8ea-dd529e940537/.user_uploaded/media_1794355112589_d837d13e.png",
    r"C:/Users/hp/.gemini/antigravity/brain/f58d96fb-8903-4428-b8ea-dd529e940537/.user_uploaded/media_1794355127163_bbe71df2.png",
    r"C:/Users/hp/.gemini/antigravity/brain/f58d96fb-8903-4428-b8ea-dd529e940537/.user_uploaded/media_1794355143043_953938e9.jpg",
    r"C:/Users/hp/.gemini/antigravity/brain/f58d96fb-8903-4428-b8ea-dd529e940537/.user_uploaded/media_1794355393598_f8cd479e.jpg",
    r"C:/Users/hp/.gemini/antigravity/brain/f58d96fb-8903-4428-b8ea-dd529e940537/.user_uploaded/media_1794355451549_0adf6575.jpg",
    r"C:/Users/hp/.gemini/antigravity/brain/f58d96fb-8903-4428-b8ea-dd529e940537/.user_uploaded/media_1794355473507_2c20c4e7.png",
    r"C:/Users/hp/.gemini/antigravity/brain/f58d96fb-8903-4428-b8ea-dd529e940537/.user_uploaded/media_1794355535359_0975e8ce.jpg",
    r"C:/Users/hp/.gemini/antigravity/brain/f58d96fb-8903-4428-b8ea-dd529e940537/.user_uploaded/media_1794355565564_40c9224e.png",
    r"C:/Users/hp/.gemini/antigravity/brain/f58d96fb-8903-4428-b8ea-dd529e940537/.user_uploaded/media_1794355591162_6eb475ce.png",
    r"C:/Users/hp/.gemini/antigravity/brain/f58d96fb-8903-4428-b8ea-dd529e940537/.user_uploaded/media_1794355607579_90454667.jpg",
    r"C:/Users/hp/.gemini/antigravity/brain/f58d96fb-8903-4428-b8ea-dd529e940537/.user_uploaded/media_1794355620919_bc29b2d0.png",
    r"C:/Users/hp/.gemini/antigravity/brain/f58d96fb-8903-4428-b8ea-dd529e940537/.user_uploaded/media_1794355668496_c0a7457b.png",
    r"C:/Users/hp/.gemini/antigravity/brain/f58d96fb-8903-4428-b8ea-dd529e940537/.user_uploaded/media_1794355696102_6cd26e40.png",
    r"C:/Users/hp/.gemini/antigravity/brain/f58d96fb-8903-4428-b8ea-dd529e940537/.user_uploaded/media_1794355714350_e89d3228.jpg",
    r"C:/Users/hp/.gemini/antigravity/brain/f58d96fb-8903-4428-b8ea-dd529e940537/.user_uploaded/media_1794355765579_0167c20f.png",
]
for i, p in enumerate(imgs, 1):
    with Image.open(p) as im:
        print(f"{i:2d}. {os.path.basename(p)}: {im.size[0]}x{im.size[1]} ({im.mode})")

for p in glob.glob("*.png") + glob.glob("*.jpg") + glob.glob("pressure_output/*.png"):
    with Image.open(p) as im:
        print(f"LOCAL {p}: {im.size[0]}x{im.size[1]} ({im.mode})")

