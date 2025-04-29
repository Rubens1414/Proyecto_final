import 'package:flutter/material.dart';
import 'package:camera/camera.dart';

class HomePage extends StatelessWidget {
  final CameraDescription camera;

  const HomePage({Key? key, required this.camera}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('App para personas con discapacidad visual'),
        centerTitle: true,
      ),
      body: Column(
        children: [
          Expanded(
            child: SizedBox.expand(
              child: ElevatedButton(
                onPressed: () {
                  Navigator.pushNamed(context, '/camera');
                },
                child: const Text(
                  'Acceder a cámara',
                  style: TextStyle(fontSize: 24),
                ),
              ),
            ),
          ),
          Expanded(
            child: SizedBox.expand(
              child: ElevatedButton(
                onPressed: () {
                  Navigator.pushNamed(context, '/instructions');
                },
                child: const Text(
                  'Instrucciones',
                  style: TextStyle(fontSize: 24),
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }
}
