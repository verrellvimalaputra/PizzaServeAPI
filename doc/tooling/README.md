# Tools used in the project
The following lists the tools and frameworks, that are used in the project. 
- [Docker](https://docs.docker.com/get-started/overview/)    
   Docker is an open platform for developing, shipping, and running applications. Docker enables you to separate your applications from your infrastructure so you can deliver software quickly. With Docker, you can manage your infrastructure in the same ways you manage your applications. By taking advantage of Docker's methodologies for shipping, testing, and deploying code, you can significantly reduce the delay between writing code and running it in production.
- [Kubernetes](https://kubernetes.io/docs/concepts/overview/)
    Kubernetes is an open-source container orchestration platform for automating the deployment, scaling, and management of containerized applications. Key components include nodes (worker machines), clusters (groups of nodes), and pods (the smallest deployable units, containing one or more containers). It helps in maintaining the availability and scalability of applications in a dynamic and efficient manner.
- [FastAPI](https://fastapi.tiangolo.com/tutorial/)
    is a versatile and developer-friendly framework that simplifies API development, embraces asynchronous programming, and ensures data validation and serialization, all while delivering high performance.
      - Easy API Creation
      - Asynchronous Support
      - Data Validation and Serialization
      - Dependency Injection
      - High Performance
- [SQLAlchemy](https://docs.sqlalchemy.org/en/20/orm/quickstart.html)
    SQLAlchemy is a powerful and popular Python library used for working with relational databases. It provides a high-level, Pythonic interface for interacting with databases, making it easier to perform database operations without writing raw SQL queries. SQLAlchemy simplifies database interaction in Python applications by providing an ORM, a high-level querying API, and support for multiple database systems. It helps developers work with databases more efficiently and maintain code that is both readable and maintainable.
- [FastAPI with SQLAlchemy](https://fastapi.tiangolo.com/tutorial/sql-databases/)
    FastAPI with SQLAlchemy are often used together in web development to create robust and efficient web applications, especially when building RESTful APIs or web services. FastAPI with SQLAlchemy provides a powerful combination for building web applications and APIs with Python. FastAPI handles the web-related aspects of your application, including request handling, data validation, and serialization, while SQLAlchemy takes care of database interactions, making it easier to create scalable, efficient, and maintainable web services.
- [Alembic](https://alembic.sqlalchemy.org/en/latest/tutorial.html)
    Alembic is a popular database migration tool for Python that is often used in conjunction with Object-Relational Mapping (ORM) libraries like SQLAlchemy. Its primary purpose is to automate and manage the process of evolving and versioning a database schema over time. Alembic is a valuable tool for managing database schema changes and ensuring that your application's database stays up-to-date as your data model evolves. It simplifies the process of creating, applying, and rolling back database schema migrations, and it is often used in combination with SQLAlchemy to maintain a smooth workflow when working with relational databases in Python applications.
- [Swagger UI](https://swagger.io/tools/swagger-ui/)
    Swagger UI is a user interface that provides a visual representation of the documentation for RESTful APIs, based on the OpenAPI Specification (formerly known as Swagger). Swagger UI is a valuable tool for API developers and consumers, providing an interactive and well-structured way to explore, test, and understand RESTful APIs. It enhances the development and integration process by providing clear, self-updating API documentation that simplifies working with and consuming APIs.

# GitLab CI/CD

The following is a collection of short hints on how to do the most essential things in a GitLab CI/CD pipeline:

- How to delay a job until another job is done: 

Use the “needs” keyword and specify which job 

Ex: 

needs: create_release_candidate

- How to change the image used in a task: 

Use the “image” keyword

Ex:

image: ruby:2.7
    
- How do you start a task manually:

Use the “when” keyword

Ex: 

when: manual

- The Script part of the config file - what is it good for?

It is used to define the commands that must be carried out as part of the job when it is executed

- If I want a task to run for every branch I put it into the stage ??

commit

- If I want a task to run for every merge request I put it into the stage ??

acceptance

- If I want a task to run for every commit to the main branch I put it into the stage ??

release

# flake8 / flakeheaven

- What is the purpose of flake8?<br>
Flake8 is used for checking code quality in Python.

- What types of problems does it detect <br>
Syntax errors, undefined names, code style violations, unused Imports and Variables

- Why should you use a tool like flake8 in a serious project?<br>
Improve project's overall quality, maintainablity.<br>
Enforce consistent coding style.<br>
Automated code review (linting).<br>
Reduce technical debt


## Run flake8 on your local Computer

  It is very annoying (and takes a lot of time) to wait for the pipeline to check the syntax 
  of your code. To speed it up, you may run it locally like this:

### Configure PyCharm (only once)
- select _Settings->Tools->External Tools_ 
- select the +-sign (new Tool)
- enter Name: *Dockerflake8*
- enter Program: *docker*
- enter Arguments: 
    *exec -i 1337_pizza_web_dev flakeheaven lint /opt/project/app/api/ /opt/project/tests/*
- enter Working Directory: *$ProjectFileDir$*

If you like it convenient: Add a button for flake8 to your toolbar!
- right click into the taskbar (e.g. on one of the git icons) and select *Customize ToolBar*
- select the +-sign and Add Action
- select External Tools->Dockerflake8

### Run flake8 on your project
  - Remember! You will always need to run the docker container called *1337_pizza_web_dev* of your project, to do this! 
    So start the docker container(s) locally by running your project
  - Now you may run flake8 
      - by clicking on the new icon in your toolbar or 
      - by selecting from the menu: Tools->External Tools->Dockerflake8 

# GrayLog

- What is the purpose of GrayLog?

Allows us to collect, index and anaylse any machine logs centrally

- What logging levels are available?

DEBUG, INFO, WARNING, ERROR, CRITICAL

- What is the default logging level?

WARNING

- Give 3-4 examples for logging commands in Python:
  ```python
  logging.debug('This message should go to the log file')
  logging.info('So should this')
  logging.warning('This is a warning')

  ```

# SonarQube

- What is the purpose of SonarQube?

SonarQube is a code quality assurance tool that performs in-depth code analysis and generates an analysis report to ensure code reliability.

- What is the purpose of the quality rules of SonarQube?

It is used to generate issues to detect bugs, code smells and security vulnerabilities. There are four types of rules:
Code smell (maintainability domain)
Bug (reliability domain)
Vulnerability (security domain)
Security hotspot (security domain)

- What is the purpose of the quality gates of SonarQube?

Quality Gates are the set of conditions a project must meet before it should be pushed to further environments. It tells us if the code meets the minimum level of quality required for the project.


## Run SonarLint on your local Computer

It is very annoying (and takes a lot of time) to wait for the pipeline to run SonarQube. 
To speed it up, you may first run the linting part of SonarQube (SonarLint) locally like this:

### Configure PyCharm for SonarLint (only once)

- Open *Settings->Plugins*
- Choose *MarketPlace*
- Search for *SonarLint* and install the PlugIn

### Run SonarLint

- In the project view (usually to the left) you can run the SonarLint analysis by a right click on a file or a folder. 
  You will find the entry at the very bottom of the menu.
- To run it on all source code of your project select the folder called *app*

# VPN

The servers providing Graylog, SonarQube and your APIs are hidden behind the firewall of Hochschule Darmstadt.
From outside the university it can only be accessed when using a VPN.
https://its.h-da.io/stvpn-docs/de/ 
