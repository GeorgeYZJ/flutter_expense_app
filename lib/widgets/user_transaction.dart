import 'package:expense_app/models/transaction.dart';
import 'package:expense_app/widgets/new_transaction.dart';
import 'package:expense_app/widgets/transaction_list.dart';
import 'package:flutter/material.dart';
import './new_transaction.dart';
import './transaction_list.dart';

class UserTranscations extends StatefulWidget {
  @override
  _UserTranscationsState createState() => _UserTranscationsState();
}

class _UserTranscationsState extends State<UserTranscations> {
  @override
  Widget build(BuildContext context) {
    return Column(
      children: <Widget>[
        NewTransaction(),
        TransactionList(),
      ],
    );
  }
}
