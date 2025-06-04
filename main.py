import os
from tkinter import Tk, Label, Button, filedialog, Text, Scrollbar, END
from PIL import Image, UnidentifiedImageError

def converter_tiff_para_pdf(pasta_origem, pasta_destino, texto_saida):
    os.makedirs(pasta_destino, exist_ok=True)
    arquivos = [f for f in os.listdir(pasta_origem) if f.lower().endswith(('.tiff', '.tif'))]

    for arquivo in arquivos:
        caminho_tiff = os.path.join(pasta_origem, arquivo)
        nome_pdf = os.path.splitext(arquivo)[0] + '.pdf'
        caminho_pdf = os.path.join(pasta_destino, nome_pdf)

        try:
            img = Image.open(caminho_tiff)
            imagens = []

            try:
                while True:
                    frame = img.copy()
                    if frame.mode in ("RGBA", "P"):
                        frame = frame.convert("RGB")
                    imagens.append(frame)
                    img.seek(img.tell() + 1)
            except EOFError:
                pass

            if imagens:
                imagens[0].save(caminho_pdf, save_all=True, append_images=imagens[1:], format='PDF')
                texto_saida.insert(END, f"✔ {arquivo} → {nome_pdf}\n")
            else:
                texto_saida.insert(END, f"⚠ Nenhuma página em {arquivo}\n")

        except UnidentifiedImageError:
            texto_saida.insert(END, f"❌ {arquivo} não é um TIFF válido.\n")
        except Exception as e:
            texto_saida.insert(END, f"❌ Erro em {arquivo}: {e}\n")

def selecionar_pasta_origem():
    pasta = filedialog.askdirectory(title="Selecionar pasta com arquivos TIFF")
    if pasta:
        label_origem.config(text=pasta)
        botao_converter.config(state="normal")

def selecionar_pasta_destino():
    pasta = filedialog.askdirectory(title="Selecionar pasta para salvar PDFs")
    if pasta:
        label_destino.config(text=pasta)

def iniciar_conversao():
    pasta_origem = label_origem.cget("text")
    pasta_destino = label_destino.cget("text")
    texto_saida.delete(1.0, END)
    converter_tiff_para_pdf(pasta_origem, pasta_destino, texto_saida)

# GUI
janela = Tk()
janela.title("Conversor TIFF para PDF")
janela.geometry("600x400")

Label(janela, text="Pasta de origem (TIFF):").pack()
label_origem = Label(janela, text="(nenhuma selecionada)", fg="blue")
label_origem.pack()
Button(janela, text="Selecionar pasta TIFF", command=selecionar_pasta_origem).pack(pady=5)

Label(janela, text="Pasta de destino (PDF):").pack()
label_destino = Label(janela, text="(nenhuma selecionada)", fg="green")
label_destino.pack()
Button(janela, text="Selecionar pasta destino", command=selecionar_pasta_destino).pack(pady=5)

botao_converter = Button(janela, text="Converter TIFF → PDF", state="disabled", command=iniciar_conversao)
botao_converter.pack(pady=10)

scroll = Scrollbar(janela)
scroll.pack(side="right", fill="y")

texto_saida = Text(janela, height=10, yscrollcommand=scroll.set)
texto_saida.pack(expand=True, fill="both")
scroll.config(command=texto_saida.yview)

janela.mainloop()