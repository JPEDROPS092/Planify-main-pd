/**
 * Utilitários para manipulação de arquivos
 * Funções para upload, download e manipulação de arquivos
 */

/**
 * Converte um arquivo para Base64
 * @param file Arquivo a ser convertido
 * @returns Promise com a string Base64
 */
export const fileToBase64 = (file: File): Promise<string> => {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = () => resolve(reader.result as string);
    reader.onerror = (error) => reject(error);
  });
};

/**
 * Converte uma string Base64 para Blob
 * @param base64 String Base64
 * @param mimeType Tipo MIME do arquivo
 * @returns Blob do arquivo
 */
export const base64ToBlob = (base64: string, mimeType: string): Blob => {
  const byteString = atob(base64.split(',')[1]);
  const ab = new ArrayBuffer(byteString.length);
  const ia = new Uint8Array(ab);
  
  for (let i = 0; i < byteString.length; i++) {
    ia[i] = byteString.charCodeAt(i);
  }
  
  return new Blob([ab], { type: mimeType });
};

/**
 * Faz o download de um arquivo
 * @param url URL do arquivo
 * @param filename Nome do arquivo para download
 */
export const downloadFile = (url: string, filename: string): void => {
  const link = document.createElement('a');
  link.href = url;
  link.download = filename;
  link.target = '_blank';
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
};

/**
 * Faz o download de um blob como arquivo
 * @param blob Blob do arquivo
 * @param filename Nome do arquivo para download
 */
export const downloadBlob = (blob: Blob, filename: string): void => {
  const url = URL.createObjectURL(blob);
  downloadFile(url, filename);
  URL.revokeObjectURL(url);
};

/**
 * Verifica se um arquivo tem uma extensão permitida
 * @param file Arquivo a verificar
 * @param allowedExtensions Array de extensões permitidas (sem ponto)
 * @returns Verdadeiro se a extensão for permitida
 */
export const isAllowedFileType = (file: File, allowedExtensions: string[]): boolean => {
  const extension = file.name.split('.').pop()?.toLowerCase() || '';
  return allowedExtensions.includes(extension);
};

/**
 * Verifica se um arquivo tem um tamanho permitido
 * @param file Arquivo a verificar
 * @param maxSizeInMB Tamanho máximo em MB
 * @returns Verdadeiro se o tamanho for permitido
 */
export const isAllowedFileSize = (file: File, maxSizeInMB: number): boolean => {
  const maxSizeInBytes = maxSizeInMB * 1024 * 1024;
  return file.size <= maxSizeInBytes;
};

/**
 * Obtém a extensão de um arquivo
 * @param filename Nome do arquivo
 * @returns Extensão do arquivo (sem ponto)
 */
export const getFileExtension = (filename: string): string => {
  return filename.split('.').pop()?.toLowerCase() || '';
};

/**
 * Obtém o tipo MIME de um arquivo com base na extensão
 * @param filename Nome do arquivo
 * @returns Tipo MIME do arquivo
 */
export const getMimeType = (filename: string): string => {
  const extension = getFileExtension(filename);
  const mimeTypes: Record<string, string> = {
    pdf: 'application/pdf',
    doc: 'application/msword',
    docx: 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    xls: 'application/vnd.ms-excel',
    xlsx: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    ppt: 'application/vnd.ms-powerpoint',
    pptx: 'application/vnd.openxmlformats-officedocument.presentationml.presentation',
    jpg: 'image/jpeg',
    jpeg: 'image/jpeg',
    png: 'image/png',
    gif: 'image/gif',
    svg: 'image/svg+xml',
    txt: 'text/plain',
    csv: 'text/csv',
    html: 'text/html',
    xml: 'application/xml',
    json: 'application/json',
    zip: 'application/zip',
    rar: 'application/x-rar-compressed',
    tar: 'application/x-tar',
    gz: 'application/gzip',
    mp3: 'audio/mpeg',
    mp4: 'video/mp4',
    avi: 'video/x-msvideo',
    mov: 'video/quicktime',
    wmv: 'video/x-ms-wmv'
  };
  
  return mimeTypes[extension] || 'application/octet-stream';
};

/**
 * Verifica se um arquivo é uma imagem
 * @param file Arquivo a verificar
 * @returns Verdadeiro se for uma imagem
 */
export const isImageFile = (file: File): boolean => {
  return file.type.startsWith('image/');
};

/**
 * Verifica se um arquivo é um documento
 * @param file Arquivo a verificar
 * @returns Verdadeiro se for um documento
 */
export const isDocumentFile = (file: File): boolean => {
  const docTypes = [
    'application/pdf',
    'application/msword',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'application/vnd.ms-excel',
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    'application/vnd.ms-powerpoint',
    'application/vnd.openxmlformats-officedocument.presentationml.presentation',
    'text/plain',
    'text/csv'
  ];
  
  return docTypes.includes(file.type);
};

/**
 * Redimensiona uma imagem
 * @param file Arquivo de imagem
 * @param maxWidth Largura máxima
 * @param maxHeight Altura máxima
 * @param quality Qualidade da imagem (0-1)
 * @returns Promise com o arquivo redimensionado
 */
export const resizeImage = (
  file: File,
  maxWidth = 1024,
  maxHeight = 1024,
  quality = 0.8
): Promise<File> => {
  return new Promise((resolve, reject) => {
    if (!isImageFile(file)) {
      reject(new Error('O arquivo não é uma imagem'));
      return;
    }
    
    const reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = (event) => {
      const img = new Image();
      img.src = event.target?.result as string;
      
      img.onload = () => {
        // Calcular novas dimensões mantendo a proporção
        let width = img.width;
        let height = img.height;
        
        if (width > maxWidth) {
          height = (height * maxWidth) / width;
          width = maxWidth;
        }
        
        if (height > maxHeight) {
          width = (width * maxHeight) / height;
          height = maxHeight;
        }
        
        // Criar canvas para redimensionar
        const canvas = document.createElement('canvas');
        canvas.width = width;
        canvas.height = height;
        
        const ctx = canvas.getContext('2d');
        if (!ctx) {
          reject(new Error('Não foi possível criar o contexto de canvas'));
          return;
        }
        
        ctx.drawImage(img, 0, 0, width, height);
        
        // Converter para blob
        canvas.toBlob(
          (blob) => {
            if (!blob) {
              reject(new Error('Não foi possível criar o blob'));
              return;
            }
            
            // Criar novo arquivo
            const newFile = new File([blob], file.name, {
              type: file.type,
              lastModified: Date.now()
            });
            
            resolve(newFile);
          },
          file.type,
          quality
        );
      };
      
      img.onerror = () => {
        reject(new Error('Erro ao carregar a imagem'));
      };
    };
    
    reader.onerror = () => {
      reject(new Error('Erro ao ler o arquivo'));
    };
  });
};

/**
 * Cria uma prévia de imagem
 * @param file Arquivo de imagem
 * @returns Promise com a URL da prévia
 */
export const createImagePreview = (file: File): Promise<string> => {
  return new Promise((resolve, reject) => {
    if (!isImageFile(file)) {
      reject(new Error('O arquivo não é uma imagem'));
      return;
    }
    
    const reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = () => resolve(reader.result as string);
    reader.onerror = (error) => reject(error);
  });
};
