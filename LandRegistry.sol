// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract LandRegistry {
    address public admin;

    struct Land {
        uint256 id;
        string location;
        uint256 area;
        uint256 price;
        address owner;
        bool isRegistered;
        string documentHash;
    }

    mapping(uint256 => Land) public lands;
    mapping(address => uint256[]) public ownerLands;
    uint256 public landCount;

    constructor() {
        admin = msg.sender;
    }

    modifier onlyAdmin() {
        require(msg.sender == admin, "Only admin can perform this action");
        _;
    }

    function registerLand(string memory _location, uint256 _area, uint256 _price, address _owner, string memory _documentHash) public onlyAdmin {
        require(_owner != address(0), "Invalid owner address");
        landCount++;
        lands[landCount] = Land(landCount, _location, _area, _price, _owner, true, _documentHash);
        ownerLands[_owner].push(landCount);
    }

    function viewLand(uint256 _landId) public view returns (uint256, string memory, uint256, uint256, address, bool, string memory) {
        Land memory land = lands[_landId];
        if (!land.isRegistered || _landId == 0 || _landId > landCount) {
            return (0, "", 0, 0, address(0), false, "");
        }
        return (land.id, land.location, land.area, land.price, land.owner, land.isRegistered, land.documentHash);
    }

    function transferOwnership(uint256 _landId, address _newOwner) public {
        Land storage land = lands[_landId];
        require(land.isRegistered, "Land not registered");
        require(msg.sender == land.owner, "Only owner can transfer");
        require(_newOwner != address(0), "Invalid new owner address");
        ownerLands[land.owner] = removeLandFromOwner(land.owner, _landId);
        land.owner = _newOwner;
        ownerLands[_newOwner].push(_landId);
    }

    function getAllLands() public view returns (Land[] memory) {
        Land[] memory allLands = new Land[](landCount);
        for (uint256 i = 1; i <= landCount; i++) {
            allLands[i - 1] = lands[i];
        }
        return allLands;
    }

    function getOwnerLands(address _owner) public view returns (uint256[] memory) {
        return ownerLands[_owner];
    }

    function removeLandFromOwner(address _owner, uint256 _landId) private view returns (uint256[] memory) {
        uint256[] memory currentLands = ownerLands[_owner];
        uint256[] memory newLands = new uint256[](currentLands.length - 1);
        uint256 index = 0;
        for (uint256 i = 0; i < currentLands.length; i++) {
            if (currentLands[i] != _landId) {
                newLands[index] = currentLands[i];
                index++;
            }
        }
        return newLands;
    }
}