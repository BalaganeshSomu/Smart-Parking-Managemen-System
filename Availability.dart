import 'package:bookyourlot/Book%20your%20lot.dart';
import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:cloud_firestore/cloud_firestore.dart';

class Availability extends StatefulWidget {
  @override
  _AvailabilityState createState() => _AvailabilityState();
}

class _AvailabilityState extends State<Availability> {
  final _firestore = FirebaseFirestore.instance;
  var mapResult = new Map();
  var x = new Map();
  String Total = '4';


  void messageStream() async {
    await for (var snapshot
        in _firestore.collection("Peelamedu - Book your Lot").snapshots()) {
      for (var i in snapshot.docs) {
        x = i.data();
      }
      print(x);
    }
  }



  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Center(
          child: Text('PEELAMEDU - PSG TECH'),
        ),
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Padding(
              padding: EdgeInsetsDirectional.fromSTEB(15, 15, 15, 0),
              child: Container(
                child: Align(
                  alignment: Alignment.center,
                  child: Text(
                    'AVAILABILITY',
                    style: GoogleFonts.varela(
                        textStyle: TextStyle(
                            fontWeight: FontWeight.bold,
                            letterSpacing: 1.5,
                            fontSize: 30)),
                  ),
                ),
              ),
            ),
            StreamBuilder<DocumentSnapshot>(
              stream: _firestore.collection("Peelamedu - Book your Lot").doc('Availability').snapshots(),
              builder: (context, snapshot) {
                final Result = snapshot.data;
                return Column(
                  children: [
                    Container(
                      margin: EdgeInsets.all(25.0),
                      decoration: BoxDecoration(
                        color: Colors.lightBlueAccent,
                        borderRadius: BorderRadius.circular(15),
                      ),
                      child: Padding(
                        padding: const EdgeInsets.all(15.0),
                        child: Column(
                          children: [
                            Padding(
                              padding: const EdgeInsets.all(10.0),
                              child: Text(
                                'Available : ${Total}',
                                style: GoogleFonts.varela(
                                    textStyle: TextStyle(
                                        color: Colors.white,
                                        fontWeight: FontWeight.bold,
                                        letterSpacing: 2,
                                        fontSize: 30)),
                              ),
                            ),
                            Padding(
                              padding: const EdgeInsets.all(10.0),
                              child: Text(
                                'Booked  : ${Result['BookedNumbers']}',
                                style: GoogleFonts.varela(
                                    textStyle: TextStyle(
                                        color: Colors.white,
                                        fontWeight: FontWeight.bold,
                                        letterSpacing: 2,
                                        fontSize: 30)),
                              ),
                            ),
                            Padding(
                              padding: const EdgeInsets.all(10.0),
                              child: Text(
                                'Free      : ${Result['AvailableNumbers']}',
                                style: GoogleFonts.varela(
                                    textStyle: TextStyle(
                                        color: Colors.white,
                                        fontWeight: FontWeight.bold,
                                        letterSpacing: 2,
                                        fontSize: 30)),
                              ),
                            ),
                            FlatButton(
                              onPressed: () {
                                messageStream();
                              },
                              child: Text(
                                'REFRESH',
                                style: GoogleFonts.varela(
                                    textStyle: TextStyle(
                                        color: Colors.black,
                                        decoration: TextDecoration.underline,
                                        letterSpacing: 1,
                                        fontSize: 11)),
                              ),
                            ),
                          ],
                        ),
                      ),
                    ),
                    Padding(
                      padding: const EdgeInsets.all(8.0),
                      child: RaisedButton(
                        child: Text('BOOK'),
                        onPressed: () {
                          if (Result['AvailableNumbers']!=0){
                            Navigator.push(
                              context,
                              MaterialPageRoute(
                                builder: (context) {
                                  return BookYourLot(); // "BOOK" is enabled if free != 0
                                },
                              ),
                            );
                          } else{
                            // "BOOK" is disabled if free != 0
                          }
                        },
                      ),
                    ),
                  ],
                );
              },
            ),
          ],
        ),
      ),
    );
  }
}
