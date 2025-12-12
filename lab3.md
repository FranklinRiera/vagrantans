
# HTTP App with Database

## Objectives

- Develop an HTTP App with access to a database
- Deploy the HTTP App and database in separate VM instances
- Use **Terraform** for the VMs deployment on AWS or Azure
- Use **Ansible** for the HTTP App configuration

## Infrastructure architecture

![](diagram1.png)


## Database

- Install a database engine on one VM. For example: `mariadb`, `postgresql`
- Create a database named `myproject`
- Create a table named `form` with the following structure


| ID | Timestamp | Remote IP | JSON |
|-|-|-|-|
| 1 | 2023-11-29 15:30 | 191.100.138.47 | {"a": "b"} |

![](table.png)

## Flask

- Create an Flask App that implements in the route `/form` both methods [POST, GET]
- **POST**: recieves JSON data and creates a new registry on the database
- **GET**: returns an html page with all the `form` table information
