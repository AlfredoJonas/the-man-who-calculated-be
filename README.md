<a name="readme-top"></a>
<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/othneildrew/Best-README-Template">
    <img src="https://truenorthinc.com/wp-content/themes/truenorth2019/images/nav-logo-black.png" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">Arithmetic Calculator REST API</h3>

  <p align="center">
    calculator service for processing basic math operations from server using token authentication!
    <br />
    <br />
    <a href="https://www.postman.com/alfredojonas/workspace/truenorth-app/overview">Postman Collection</a>
    ·
    <a href="https://github.com/othneildrew/Best-README-Template/issues">Report Bug</a>
    ·
    <a href="https://github.com/othneildrew/Best-README-Template/issues">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

### System, model and api Design

![System design][system-design]

![Api design][api-design]

Service platform to provide a simple calculator functionality (addition, subtraction,
multiplication, division, square root, and a random string generation) where each functionality will
have a separate cost per request.

User’s will have a starting credit/balance. Each request will be deducted from the user’s balance.
If the user’s balance isn’t enough to cover the request cost, the request shall be denied.

<p align="right">(<a href="#readme-top">back to top</a>)</p>


### Built With


* [![Django][django]][django-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running follow these simple example steps.

### Prerequisites

This is a dockerized project, in terms of build this up you'll need to have already installed and configured Docker on your machine.
* <a href="https://docs.docker.com/desktop/?_gl=1*16tppjw*_ga*MTM2MTA3NTk5NC4xNjg1OTE4NTA0*_ga_XJWPQMJYHQ*MTY4NzI3MTMzMy4xMi4xLjE2ODcyNzEzNjkuMjQuMC4w">Install and configure Docker</a>

### Installation

_You can follow this steps in order to have an app build and up._

1. Clone this repo
   ```sh
   git clone https://github.com/AlfredoJonas/the-man-who-calculated-be
   ```
2. Move on the root dir of your project
    ```sh
    cd the-man-who-calculated-be
    ```
3. Do a copy of the *env.example* file renaming it as *.env*
   ```sh
   cp .env.example .env
   ```
4. Now just build the app using docker, in this case we encapsuled all the required steps in a single makefile command, so just type...
   ```sh
   make appsetup
   ``` 
5. Run tests to confirm everything is OK
    ```sh
    docker-compose run web pytest
    ```
6. To lift the app use docker as usual running
    ```sh
    docker-compose up
    ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- CONTACT -->
## Contact

Jonas Gonzalez - [@Sanoj94](https://twitter.com/Sanoj94) - alfredojonas94@gmail.com

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

Resources I find helpful and would like to give credit to.

* [Django docs](https://docs.djangoproject.com/en/4.2/)
* [Docker for django admin](https://github.com/docker/awesome-compose/tree/master/official-documentation-samples)
* [PyTests on Django](https://pytest-django.readthedocs.io/en/latest/)
* [StackOverflow](https://stackoverflow.com/)


<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[django]: https://img.shields.io/badge/Django-103e2e?style=for-the-badge&logo=django&logoColor=white
[django-url]: https://www.djangoproject.com/
[system-design]: DataModelAndSystemChart.png
[api-design]: apiDesign.png