from http.server import BaseHTTPRequestHandler
import traceback

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            # ¡Truco! Importamos las librerías justo aquí adentro
            # para que el servidor no falle al inicializarse.
            import qrcode
            import io
            import urllib.parse
            
            parsed_path = urllib.parse.urlparse(self.path)
            query_params = urllib.parse.parse_qs(parsed_path.query)
            text_to_encode = query_params.get('text', ['https://github.com'])[0]
            
            qr = qrcode.QRCode(version=1, box_size=10, border=4)
            qr.add_data(text_to_encode)
            qr.make(fit=True)
            
            img = qr.make_image(fill_color="black", back_color="white")
            buffered = io.BytesIO()
            img.save(buffered, format="PNG")
            
            self.send_response(200)
            self.send_header('Content-type', 'image/png')
            self.end_headers()
            self.wfile.write(buffered.getvalue())
            
        except Exception as e:
            # Ahora sí, si falla la importación, lo imprimirá en texto blanco
            error_msg = traceback.format_exc()
            self.send_response(500)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(f"Error detectado:\n{error_msg}".encode('utf-8'))
        return
