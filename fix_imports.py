# corrigir_notification.py

# Lista de arquivos afetados
arquivos = [
    "/home/jpcode092/projects/Planify-main-pd/frontend/pages/projetos/[id]/planning/sprints.vue",
    "/home/jpcode092/projects/Planify-main-pd/frontend/pages/projetos/[id]/settings/index.vue",
    "/home/jpcode092/projects/Planify-main-pd/frontend/pages/projetos/[id]/communication/messages.vue",
    "/home/jpcode092/projects/Planify-main-pd/frontend/pages/projetos/[id]/communication/notifications.vue",
    "/home/jpcode092/projects/Planify-main-pd/frontend/pages/projetos/[id]/communication/index.vue",
    "/home/jpcode092/projects/Planify-main-pd/frontend/pages/projetos/[id]/tasks/new.vue",
    "/home/jpcode092/projects/Planify-main-pd/frontend/pages/projetos/[id]/tasks/kanban.vue",
    "/home/jpcode092/projects/Planify-main-pd/frontend/pages/projetos/[id]/tasks/index.vue",
    "/home/jpcode092/projects/Planify-main-pd/frontend/pages/projetos/[id]/tasks/gantt.vue",
    "/home/jpcode092/projects/Planify-main-pd/frontend/pages/projetos/[id]/team/permissions.vue",
    "/home/jpcode092/projects/Planify-main-pd/frontend/pages/projetos/[id]/team/index.vue",
    "/home/jpcode092/projects/Planify-main-pd/frontend/pages/projetos/[id]/resources/documents/upload.vue",
    "/home/jpcode092/projects/Planify-main-pd/frontend/pages/projetos/[id]/resources/documents/index.vue",
    "/home/jpcode092/projects/Planify-main-pd/frontend/pages/projetos/[id]/resources/costs/new.vue",
    "/home/jpcode092/projects/Planify-main-pd/frontend/pages/projetos/[id]/resources/costs/index.vue",
    "/home/jpcode092/projects/Planify-main-pd/frontend/pages/projetos/[id]/resources/risks/new.vue",
    "/home/jpcode092/projects/Planify-main-pd/frontend/pages/projetos/[id]/resources/risks/index.vue",
    "/home/jpcode092/projects/Planify-main-pd/frontend/pages/projetos/[id]/reports/risks.vue",
    "/home/jpcode092/projects/Planify-main-pd/frontend/pages/projetos/[id]/reports/export.vue",
    "/home/jpcode092/projects/Planify-main-pd/frontend/pages/projetos/[id]/reports/index.vue",
    "/home/jpcode092/projects/Planify-main-pd/frontend/pages/projetos/[id]/reports/tasks.vue",
    "/home/jpcode092/projects/Planify-main-pd/frontend/pages/projetos/[id]/reports/costs.vue",
    "/home/jpcode092/projects/Planify-main-pd/frontend/pages/projetos/[id]/index.vue"
]

# Substituição alvo
alvo = "from '@/composables/useNotification'"
substituto = "from '@/stores/composables/useNotification'"

def corrigir_importacoes():
    for caminho in arquivos:
        try:
            with open(caminho, "r", encoding="utf-8") as f:
                conteudo = f.read()

            if alvo in conteudo:
                novo_conteudo = conteudo.replace(alvo, substituto)
                with open(caminho, "w", encoding="utf-8") as f:
                    f.write(novo_conteudo)
                print(f"✔ Corrigido: {caminho}")
            else:
                print(f"⏭ Nada para corrigir: {caminho}")
        except Exception as e:
            print(f"❌ Erro ao processar {caminho}: {e}")

if __name__ == "__main__":
    corrigir_importacoes()
