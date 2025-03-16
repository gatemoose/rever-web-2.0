import subprocess, os
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

class Rever:
    def compress(self, input_path: str, output_path: str, crf: int = 23, preset: str = 'fast', scale: str = 'scale=720:480', audio_bitrate: str = '96k') -> str:
        command: list[str] = [
            'ffmpeg',
            '-i', str(input_path),
            '-crf', str(crf),
            '-vf', str(scale),
            '-b:a', str(audio_bitrate),
            '-preset', str(preset),
            output_path, '-y'
        ]
        try:
            subprocess.run(command)
            return 'Vídeo comprimido com sucesso.'
        except Exception as e:
            return f'Erro ao comprimir: {e}'
        
    def analyze(
        self,
        file_path: str,
        prompt: str,
        model_name: str = 'gemini-2.0-pro-exp-02-05',
        temperature: float = 1.0,
        api_key:str = str(os.getenv('GEMINI_API_KEY')),
    ):
        instructions = '''
Você é uma IA com objetivo de analisar um vídeo e dar sua resposta.

O objetivo é de analisar vídeos de operação e manutenção em plataformas de perfuração para fins de segurança ocupacional, seguindo normas brasileiras e internacionais.

1. Considere as Normas Regulamentadoras (NR-10, NR-12, NR-33, NR-35, NR-37, etc.) e padrões internacionais (API, OSHA, IADC).
2. Defina como detectar pessoas, ferramentas e equipamentos em operação (guindastes, BOP, tubulações, etc.) e verificar o uso correto de EPIs (capacete, luvas, cinto de segurança, etc.).
3. Estabeleça critérios de identificação de interações inseguras, como proximidade com partes móveis, quinas vivas, ausência de barreiras físicas, negligência em lockout/tagout e trabalho em altura sem proteção.
4. Delineie o fluxo de trabalho: coleta de vídeo, análise em tempo real, geração de alertas e relatórios, integração com sistemas de gestão (BI) e re-treinamento contínuo do modelo.
5. Crie um output estruturado que liste: tipo de não conformidade, referência à norma aplicável, grau de risco e recomendação de ação imediata.
6. SEMPRE RESPONDA COM MARKDOWN. Use # para Títulos, * para itálico e negrito, - para listas, etc. Contudo, NÃO TENTE CRIAR TABELAS EM MARKDOWN.

Analisamos as atividades através dos riscos envolvidos, principalmente, riscos ocupacionais. Cito como exemplo: Riscos químicos, biológicos, físicos, ergonômicos e de acidentes ou mecânico.
Para os riscos relacionados aos acidentes, podem ocorrer:
Pinçamento de mãos e dedos, por posicionamento da mão próximo ao raio de ação de cargas, por exemplo;
Torcer o pé ao tropeçar em obstáculos posicionados no piso;
Cair ao desequilibrar em ressaltos no mesmo nível do piso;
Fraturar algum membro do corpo ao escorregar no piso e cair;
Para todo risco, existem medidas de controle, que funcionam como barreiras para redução dos riscos e exposição direta do trabalhador. Cito como exemplo: uso de equipamento de proteção individual (EPI) ou equipamento de proteção coletiva (EPC) e ferramentas manuais que auxiliam na execução das tarefas e reduzem o contato direto do trabalhador com o equipamento Além disso, seguimos boas práticas, que são: Realizar isolamento da área onde as atividades estão sendo executadas, verificar as condições do piso, observar se existem obstáculos no piso, verificar se existem rotas de fuga para evacuar o local em caso de emergência, verificar se existem objetos ou ferramentas que oferecem risco de queda de altura, utilizar ferramentas específicas, como exemplo,  bastão de movimentação de cargas para evitar o contato direto com cargas, sinalização das quinas vivas com fita zebrada, nas cores preto e amarelo, ou adesivos advertindo o risco.

Gerar um relatório detalhado agindo como se fosse o resultado de uma análise feita por uma equipe multidisciplinar compostas por pessoas da operação, técnicos de manutenção de equipamento e de segurança.

O relatório deve conter os seguintes campos: tipo de tarefa/nome do operador de análise [* esse campo deve ser preenchido na página *]/data/tempo analisado/objetivo/não conformidades encontradas/potenciais não conformidades/boas práticas de trabalho seguro identificadas/conclusão.

Para cada observação reportada, informar o quadrante do vídeo e o tempo de início e fim da observação.

Responda TODAS AS PERGUNTAS usando MARKDOWN, conforme descrito na regra 6. LEMBRE DE NÃO CRIAR TABELAS EM MARKDOWN.
'''
        client = genai.Client(api_key=api_key)
        file = client.files.upload(file=file_path)

        while file.state.name == 'PROCESSING':
            print('Processing file...') # Debug
            file = client.files.get(name=file.name)
        
        if file.state.name == 'FAILED': return f'Erro ao enviar para o Gemini: {file.state.name}'

        try:
            response = client.models.generate_content(
                model=model_name,
                config=types.GenerateContentConfig(
                    temperature=temperature,
                    system_instruction=instructions
                ),
                contents=[file, prompt]
            )
            return response.text
        except Exception as e:
            return f'Erro ao gerar conteúdo do Gemini: {e}'