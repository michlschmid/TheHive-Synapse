# TheHive-Synapse

Last update: 2020-05-05

## Automatic EMail Notifications
Goal: Send automatic Email notifications to a set of configured email addresses.
Trigger events:
* Alert creation
* Case creation
* Case Task start, stop for all Tasks
* Case TaskLog updates for all Tasks named "Communication" (task name shall be configurable)
* Case closing

Email contents:
* Subject:
 * Configurable prefix
 * Alerts: ... #ALERT-ID RAISED
 * Cases:
  * ... #CASE-ID CREATED | CLOSED
  * ... #CASE-ID TASKNAME STARTED | UPDATED | CLOSED
