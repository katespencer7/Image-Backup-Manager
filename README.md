### Image-Backup-Manager (temp name)
### Project for CS407
---
##### An app that backs up photos and uses digital forensic techniques to verify image files and detect file tampering, editing, or corrosion over time. Uses the 3-2-1 rule of data protection: 3 copies of data, 2 different mediums (two file locations, or better, two different drives/disks), and 1 offsite backup (i.e. cloud). When photos are uploaded, the app stores a SHA-256 hash of each file to verify that everything has been copied over correctly. These hashes are stored in a SQLite database. This app includes an interface to add/delete photos. 
---
Requirements: 
PyQt5
SQLite
