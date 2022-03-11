import 'package:flutter/material.dart';
import 'dart:math' as math;

void main() {
    runApp(const MyApp());
}

class MyApp extends StatelessWidget {
    const MyApp({Key? key}) : super(key: key);

    @override
    Widget build(BuildContext context) {
        return const MaterialApp(
            title: 'Mochi\'s To Do List',
            home: RandomWords(),
        );
    }
}

class RandomWords extends StatefulWidget {
    const RandomWords({Key? key}) : super(key: key);

    @override
    _RandomWordsState createState() => _RandomWordsState();
}

class _RandomWordsState extends State<RandomWords> {
    final _task = <String>[];
    final _taskCompleted = <bool>[];
    final _biggerFont = const TextStyle(fontSize: 18.0);
    final _random = math.Random();
    final List<String> _verbs = ['Hug',
                                 'Kiss',
                                 'Wash',
                                 'Complain to',
                                 'Sue',
                                 'Play Golf with',
                                 'Have Dinner with'];
    final List<String> _nouns = ['Nibbles',
                                 'Bella',
                                 'Coworker',
                                 'Sister',
                                 'Mom',
                                 'Dad',
                                 'Google Fi'];

    @override
    Widget build(BuildContext context) {
        return Scaffold(
            appBar: AppBar(
                title: const Text('Mochi\'s To Do List'),
            ),
            body: ListView.builder(
                padding: const EdgeInsets.all(16.0),
                itemBuilder: (context, i) {
                    if (i.isOdd) return const Divider();

                    final index = i ~/ 2;
                    if (index >= _task.length) {
                        final _randomTask = _verbs[_random.nextInt(_verbs.length)] + ' '
                                             + _nouns[_random.nextInt(_nouns.length)];
                        _task.add(_randomTask);
                        _taskCompleted.add(false);
                    }
                    return CheckboxListTile(
                        title: Text(
                            _task[index],
                            style: _biggerFont,
                        ),
                        value: _taskCompleted[index],
                        onChanged: (newValue) {
                            setState(() {
                                _taskCompleted[index] = newValue!;
                            });
                        },
                    );
                },
            ),
        );
    }
}
