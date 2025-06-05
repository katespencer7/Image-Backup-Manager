### TripleCheck: An Image Backup Manager
### Project for CS407 Spring 2025
![Logo](assets/logo.png)
---
##### An app that backs up photos using digital forensic techniques to verify image files and detect file tampering, editing, or corrosion over time. TripleCheck uses the 3-2-1 rule of data protection: 3 copies of data, 2 different mediums (two file locations, or better, two different drives/disks), and 1 offsite backup (i.e. cloud). When photos are uploaded, the app stores a SHA-256 hash of each file to verify that everything has been copied over correctly. These hashes are stored in a json file. This app includes an interface to add/delete photos to/from the current working directory. 
---
Requirements: 
PyQt5, Pillow
