# Item Catalog
This application provides a list of items within a variety of categories as well as provide a user registration and authentication system. Registered users will have the ability to post, edit and delete their own items.


## Getting Started

### prerequisite
* [VirtualBox](https://www.virtualbox.org/)
* [Vagrant](https://www.vagrantup.com/)

### Install
In terminal type:
`git clone https://github.com/hraldur/catalog.git`

## Usage

1. Open terminal and browse vagrant folder
2. To star the Virtual Machine type in terminal `vagrant up`
3. When `vagrant up` is finished running you can run `vagrant ssh` to log into Linux Virtual Machine
4. Change folder `cd /vagrant/catalog`
5. Run project `python run_server.py`
6. open `http://localhost:5000/` in your browser
