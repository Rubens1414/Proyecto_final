import 'dart:convert';
import 'package:http/http.dart' as http;

class APIService {
  static const String _baseUrl = 'http://52.87.187.89:8000';

  static Future<bool> sendImage(String base64Image) async {
    try {
      final response = await http.post(
        Uri.parse('$_baseUrl/predict'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({'image': base64Image}),
      );
      return response.statusCode == 200;
    } catch (e) {
      print('Error al enviar la imagen: $e');
      return false;
    }
  }

  static Future<String?> fetchInterpretation() async {
    try {
      final response = await http.get(Uri.parse('$_baseUrl/interpretation'));
      if (response.statusCode == 200) {
        final utf8DecodedBody = utf8.decode(response.bodyBytes);
        final data = jsonDecode(utf8DecodedBody);
        return data['interpretation'] ?? "No se pudo obtener interpretación.";
      } else {
        return null;
      }
    } catch (e) {
      print('Error al obtener la interpretación: $e');
      return null;
    }
  }
}
