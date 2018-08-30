# Telephone Calls API

This HTTP REST API receives call detail records and calculates monthly bills for a given telephone number.

The API avoids consistency errors when receiving call records, eliminating the concerns of telecommunication platforms that consume the service.

This service expects Start/End call record pairs inputs. Then, counts bills based of pre-existent charge prices. On the final month period, a Bill is avaliable for query with all call records information of subscribers by monthly period.

## Instalation
