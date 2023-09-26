pragma solidity 0.6.0;

contract CommodityContract {
    struct Commodity {
        address seller;
        address buyer;
        uint cost;
        uint quantity;
        bool isPaid;
        bool isDelivered;
    }

    mapping(uint => Commodity) public commodities;
    uint public nextCommodityId;

    constructor() public {
        nextCommodityId = 1;
    }

    function createCommodity(address _seller, uint _cost, uint _quantity) external {
        commodities[nextCommodityId] = Commodity(_seller, address(0), _cost, _quantity, false, false);
        nextCommodityId++;
    }

    function purchase(uint _commodityId) external payable {
        require(_commodityId < nextCommodityId, "Invalid commodity ID");
        Commodity storage commodity = commodities[_commodityId];

        require(msg.value == commodity.cost, "Please pay the exact amount");
        require(!commodity.isPaid, "Transaction Completed");

        commodity.buyer = msg.sender;
        commodity.isPaid = true;
    }

    function deliver(uint _commodityId) external {
        require(_commodityId < nextCommodityId, "Invalid commodity ID");
        Commodity storage commodity = commodities[_commodityId];

        require(commodity.isPaid, "Transaction Incomplete");
        require(!commodity.isDelivered, "Commodity has already been delivered");
        require(msg.sender == commodity.seller, "Only Seller can deliver the commodity");

        commodity.isDelivered = true;
    }
}
