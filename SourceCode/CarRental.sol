pragma solidity >= 0.8.11 <= 0.8.11;

contract CarRental {
    string public users;
    string public car_details;
    string public rental_details;

    //function to save user details to Blockchain
    function addUsers(string memory u) public {
        users = u;	
    }
    //call to get user details details	
    function getUsers() public view returns (string memory) {
        return users;
    }

    //function to save car details in Blockchain
    function addCars(string memory cd) public {
        car_details = cd;	
    }
    //call to get car details	
    function getCars() public view returns (string memory) {
        return  car_details;
    }
    //function to save rent details
    function setRentals(string memory rd) public {
        rental_details = rd;	
    }
    //return tramsaction details
    function getRentals() public view returns (string memory) {
        return rental_details;
    }

    constructor() public {
        users = "";
	rental_details = "";
	car_details = "";
    }
}