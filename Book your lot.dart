import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'Terms and Conditions.dart';
import 'package:cloud_firestore/cloud_firestore.dart';
import 'Success.dart';
class BookYourLot extends StatefulWidget {
  @override
  _BookYourLotState createState() => _BookYourLotState();
}

class _BookYourLotState extends State<BookYourLot> {
  final _formKey = GlobalKey<FormState>();
  final VehicleNumber = TextEditingController();
  final Timing = TextEditingController();
  String dropdownValue = 'CAR - 4 WHEELER';
  final _firestore = FirebaseFirestore.instance;
  var x = new Map();

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Padding(
          padding: const EdgeInsets.all(0.0),
          child: Center(
            child: Text(
              'BOOK YOUR LOT',
              style: GoogleFonts.varela(
                  textStyle: TextStyle(
                      fontWeight: FontWeight.bold,
                      letterSpacing: 2,
                      fontSize: 25)),
            ),
          ),
        ),
      ),
      body: Form(
        key: _formKey,
        child: Column(
          mainAxisAlignment: MainAxisAlignment.start,
          children: <Widget>[
            // Add TextFormFields and ElevatedButton here.
            Container(
              child: Padding(
                padding: EdgeInsetsDirectional.fromSTEB(10, 10, 10, 0),
                child: Container(
                  child: Align(
                    alignment: Alignment.centerLeft,
                    child: Text(
                      'LICENSE PLATE NUMBER',
                      style: GoogleFonts.varela(
                          textStyle: TextStyle(
                              fontWeight: FontWeight.bold,
                              letterSpacing: 1,
                              fontSize: 20)),
                    ),
                  ),
                ),
              ),
            ),
            Padding(
              padding: const EdgeInsets.all(10.0),
              child: TextFormField(
                controller: VehicleNumber,
                decoration: InputDecoration(
                  hintText: 'ENTER WITHOUT SPACE',
                  filled: true,
                  fillColor: Colors.blueGrey[250],
                  icon: Icon(
                    Icons.compare_arrows,
                    color: Colors.blue[600],
                  ),
                  border: OutlineInputBorder(
                    borderRadius: BorderRadius.all(Radius.circular(10.0)),
                    borderSide: BorderSide.none,
                  ),
                ),
                validator: (value) {
                  if (value.isEmpty) {
                    return 'Please enter some text';
                  }
                  return null;
                },
              ),
            ),
            Container(
              child: Padding(
                padding: EdgeInsetsDirectional.fromSTEB(10, 0, 10, 0),
                child: Container(
                  child: Align(
                    alignment: Alignment.centerLeft,
                    child: Text(
                      'VEHICLE TYPE',
                      style: GoogleFonts.varela(
                          textStyle: TextStyle(
                              fontWeight: FontWeight.bold,
                              letterSpacing: 1,
                              fontSize: 20)),
                    ),
                  ),
                ),
              ),
            ),
            Padding(
              padding: const EdgeInsets.all(5.0),
              child: TextFormField(
                enabled: false,
                decoration: InputDecoration(
                  hintText: ' CAR - 4 WHEELER ',
                  filled: true,
                  fillColor: Colors.blueGrey[250],
                  icon: Icon(
                    Icons.directions_car,
                    color: Colors.blue[600],
                  ),
                  border: OutlineInputBorder(
                    borderRadius: BorderRadius.all(Radius.circular(10.0)),
                    borderSide: BorderSide.none,
                  ),
                ),
              ),
            ),

            Container(
              child: Padding(
                padding: EdgeInsetsDirectional.fromSTEB(10, 0, 10, 0),
                child: Container(
                  child: Align(
                    alignment: Alignment.centerLeft,
                    child: Text(
                      'START TIME',
                      style: GoogleFonts.varela(
                          textStyle: TextStyle(
                              fontWeight: FontWeight.bold,
                              letterSpacing: 1,
                              fontSize: 20)),
                    ),
                  ),
                ),
              ),
            ),
            Padding(
              padding: const EdgeInsets.all(5.0),
              child: TextFormField(
                enabled: false,
                decoration: InputDecoration(
                  hintText: ' FROM NOW ',
                  filled: true,
                  fillColor: Colors.blueGrey[250],
                  icon: Icon(
                    Icons.timer,
                    color: Colors.blue[600],
                  ),
                  border: OutlineInputBorder(
                    borderRadius: BorderRadius.all(Radius.circular(10.0)),
                    borderSide: BorderSide.none,
                  ),
                ),
              ),
            ),
            Container(
              child: Padding(
                padding: EdgeInsetsDirectional.fromSTEB(10, 0, 10, 0),
                child: Container(
                  child: Align(
                    alignment: Alignment.centerLeft,
                    child: Text(
                      'TIMING',
                      style: GoogleFonts.varela(
                          textStyle: TextStyle(
                              fontWeight: FontWeight.bold,
                              letterSpacing: 1,
                              fontSize: 20)),
                    ),
                  ),
                ),
              ),
            ),
            Padding(
              padding: const EdgeInsets.all(5.0),
              child: TextFormField(
                controller: Timing,
                decoration: InputDecoration(
                  hintText: 'ENTER IN MINUTES',
                  filled: true,
                  fillColor: Colors.blueGrey[250],
                  icon: Icon(
                    Icons.access_time,
                    color: Colors.blue[600],
                  ),
                  border: OutlineInputBorder(
                    borderRadius: BorderRadius.all(Radius.circular(10.0)),
                    borderSide: BorderSide.none,
                  ),
                ),
                validator: (value) {
                  if (value.isEmpty) {
                    return 'Please enter some text';
                  }
                  return null;
                },
              ),
            ),
            Padding(
              padding: const EdgeInsets.all(0.0),
              child: RaisedButton(
                child: Text('PAY'),
                onPressed: () {
                  if (_formKey.currentState.validate()) {
                    _firestore
                        .collection("Peelamedu - Book your Lot")
                        .doc('Availability')
                        .get()
                        .then((value) {
                      var map = new Map();
                      dynamic AvailableList = [];
                      dynamic BookedList = [];
                      dynamic Alloted;
                      var listA = new List();
                      var listB = new List();
                      map = value.data();
                      AvailableList = map['Available'];
                      BookedList = map['Booked'];
                      Alloted = AvailableList.removeLast();
                      BookedList.add(Alloted);
                      listA = AvailableList;
                      listB = BookedList;
                      map['AvailableNumbers'] = listA.length;
                      map['BookedNumbers'] = listB.length;
                      map['Available'] = AvailableList;
                      _firestore
                          .collection("Peelamedu - Book your Lot")
                          .doc('Availability')
                          .update(map);
                      _firestore
                          .collection("Peelamedu - Book your Lot")
                          .doc(Alloted.toString())
                          .update(
                        {
                          'VehicleNumber': VehicleNumber.text,
                          'time': Timestamp.now(),
                          'paid': int.parse(Timing.text),
                          'EntryStatus': false,
                        },
                      );
                      _firestore
                          .collection('Peelamedu - Book your Lot')
                          .doc('Balance')
                          .get()
                          .then((value) {
                        var map = new Map();
                        map = value.data();
                        dynamic CurrentBal;
                        CurrentBal = map['CurrentBalance'].toString();
                        CurrentBal = double.parse(CurrentBal) -
                            int.parse(Timing.text) * 0.5;
                        map['CurrentBalance'] = CurrentBal;
                        _firestore
                            .collection("Peelamedu - Book your Lot")
                            .doc('Balance')
                            .update(map);
                        Navigator.push(
                          context,
                          MaterialPageRoute(
                            builder: (context) {
                              return Success();
                            },
                          ),
                        );
                      });
                    });
                  }
                },
              ),
            ),
            FlatButton(
              child: Text(
                'TERMS AND CONDITIONS',
                style: GoogleFonts.varela(
                    textStyle: TextStyle(
                        color: Colors.blue,
                        decoration: TextDecoration.underline,
                        letterSpacing: 1,
                        fontSize: 12)),
              ),
              onPressed: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(
                    builder: (context) {
                      return TermsAndConditions();
                    },
                  ),
                );
              },
            ),
          ],
        ),
      ),
    );
  }
}
