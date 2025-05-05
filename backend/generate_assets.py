from PIL import Image, ImageDraw, ImageFont
import os

def create_logo():
    """Cria o logo do Planify"""
    # Criar uma imagem 200x200 com fundo transparente
    img = Image.new('RGBA', (200, 200), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Desenhar um círculo azul
    draw.ellipse([20, 20, 180, 180], fill='#2196F3')
    
    # Desenhar a letra P em branco
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 120)
    except:
        font = ImageFont.load_default()
    
    draw.text((60, 30), "P", fill='white', font=font)
    
    # Salvar o logo
    img.save('static/img/logo.png')
    img_small = img.resize((32, 32))
    img_small.save('static/img/favicon.ico')

def create_default_avatar():
    """Cria um avatar padrão para usuários"""
    # Criar uma imagem 100x100 com fundo azul claro
    img = Image.new('RGB', (100, 100), '#BBDEFB')
    draw = ImageDraw.Draw(img)
    
    # Desenhar um círculo cinza para representar a pessoa
    draw.ellipse([35, 20, 65, 50], fill='#757575')  # cabeça
    draw.rectangle([30, 50, 70, 90], fill='#757575')  # corpo
    
    # Salvar o avatar
    img.save('static/img/default_avatar.png')

def create_project_icons():
    """Cria ícones para diferentes tipos de projetos"""
    icons = {
        'iot': '🔌',
        'ml': '🤖',
        'ar': '👓',
        'automation': '⚙️',
        'blockchain': '🔗'
    }
    
    for name, emoji in icons.items():
        # Criar uma imagem 64x64 com fundo transparente
        img = Image.new('RGBA', (64, 64), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 40)
        except:
            font = ImageFont.load_default()
        
        # Desenhar o emoji
        draw.text((12, 12), emoji, font=font)
        
        # Salvar o ícone
        img.save(f'static/img/project_{name}.png')

def create_status_icons():
    """Cria ícones para diferentes status"""
    statuses = {
        'pending': ('⏳', '#FFA000'),  # âmbar
        'in_progress': ('🔄', '#2196F3'),  # azul
        'completed': ('✅', '#4CAF50'),  # verde
        'blocked': ('⛔', '#F44336'),  # vermelho
    }
    
    for name, (emoji, color) in statuses.items():
        # Criar uma imagem 32x32 com fundo transparente
        img = Image.new('RGBA', (32, 32), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24)
        except:
            font = ImageFont.load_default()
        
        # Desenhar o emoji
        draw.text((4, 4), emoji, font=font)
        
        # Salvar o ícone
        img.save(f'static/img/status_{name}.png')

def main():
    """Função principal para gerar todos os assets"""
    # Criar diretório de static/img se não existir
    os.makedirs('static/img', exist_ok=True)
    
    print("Gerando assets...")
    
    print("Criando logo...")
    create_logo()
    
    print("Criando avatar padrão...")
    create_default_avatar()
    
    print("Criando ícones de projetos...")
    create_project_icons()
    
    print("Criando ícones de status...")
    create_status_icons()
    
    print("Assets gerados com sucesso!")

if __name__ == '__main__':
    main()
