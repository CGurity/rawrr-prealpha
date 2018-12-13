# RAWRR - Pre Alpha
(Risk Assessment oriented Workflow and Recommendation Roadmap builder)

This project was developed for personal use as a pilot to test the data collection on organizational security assessments based on the [SAFETAG Framework](https://safetag.org), this software is intended to be rewritten in a different language and with better standards, however, the features offered are functional:
- Support for multiple organizations
- Documentation of risk matrix exercise
- Documentation of assessment activities
- Documentation of vulnerabilities
- Documentation of recommendations and implementation roadmaps
- Report generation

## Prerequisites and instalation
- Python3 with pip
- Gettext (Probably already installed in Linux)
- Django 2
- Some django extensions like Markdown Filter and Widget Tweaks

For a debian based distro (including Ubuntu, Linux Mint, Kali, etc.) the following can be pasted on a terminal with root privileges:

```bash
apt install python3 gettext
pip3 install Django django-markdown-filter django-widget-tweaks
```

## Usage
- This software is used through the Django builtin test server, that must be enough given that is not designed to be used for many people
  - Normal: ```python3 manage.py runserver``` and open in a browser http://127.0.0.1:8000
  - Accesible from network: ```python3 manage.py runserver 0.0.0.0:8000``` and open in the same machine the same link than abobe and from any other machine in the network http://ip-address-of-the-machine-with-the-sotware:8000
- Every view require the user to be authenticated:
  - **user:** rawrr
  - **password:** givememyworkflow
- Use the GUI. There is some preloaded random data to see the structure of the tool, is recommended to create a second organization to start filling real information in a fast way

## Security considerations
- This tool is designed to run in the Django's test server just when is meant to be used. Serving it in a full production server could lead to data compromise.
- The database used to store the information doesn't have any encryption in place, in case of doubt the directory with the application and the database can work inside an encrypted volume of Veracrypt or similar
- In case of using this tool on a shared network environment is worth noting that the data transmited to and from other devices to the computer with the tool installed can be visible as cleartext by anyone sniffing the network traffic, such as admins, attackers, etc. Don't use this tool to store sensitive information with the network server open if you don't trust the network users.

## Functionality Considerations
- The software must have bugs at this moment, be aware of them
- The tool must run in Linux, MacOS or Windows as long as the dependences are met. The development was made in Ubuntu and Linux Mint.
- To the moment some actions must be done through the Django admin interface in ```/admin```, for example:
  - Manage implementation terms
  - Full management of organizations
- Right now there is partial support for translations, all the interfaces are in English and the reports can be generated in English and Spanish, the language can be defined in the template ```base_report.html``` on the third line, it could be 'en' or 'es'
- More languages can be added using the Django standard workflow (Quick guide TBD)
- The HTML report is made to be saved as a complete website for delivery, using Mozilla Firefox is recommended for that, given its better management of relative links used for table of content and internal references
