pragma solidity >= 0.8.11 <= 0.8.11;
pragma experimental ABIEncoderV2;
//Bidding solidity code
contract Insure {

    uint public userCount = 0; 
    mapping(uint => user) public userList; 
     struct user
     {
       string username;
       string password;
       string phone;
       string email;
       string user_address;
     }
 
   // events 
   event userCreated(uint indexed _userId);
   
   //function  to save user details to Blockchain
   function saveUser(string memory uname, string memory pass, string memory phone, string memory email, string memory add) public {
      userList[userCount] = user(uname, pass, phone, email, add);
      emit userCreated(userCount);
      userCount++;
    }

     //get user count
    function getUserCount()  public view returns (uint) {
          return  userCount;
    }

    uint public policyCount = 0; 
    mapping(uint => policy) public policyList; 
     struct policy
     {
       string policy_id;
       string policy_name;
       string insurance_amount;
       string purchase_amount;
       string covered_duration;
       string description;   
       string provider_name;       
     }
 
   // events 
   event policyCreated(uint indexed _auctionId);
   
   //function  to save policy details to Blockchain
   function savePolicy(string memory pid, string memory pname, string memory ins_amount, string memory pur_amount, string memory duration, string memory desc, string memory provider) public {
      policyList[policyCount] = policy(pid, pname, ins_amount, pur_amount, duration, desc, provider);
      emit policyCreated(policyCount);
      policyCount++;
    }

    //get policy count
    function getPolicyCount()  public view returns (uint) {
          return  policyCount;
    }

    uint public purchaseCount = 0; 
    mapping(uint => purchase) public purchaseList; 
     struct purchase
     {
       string username;
       string insurance_id;
       string purchase_date;
       string claim_details;
     }
 
   // events 
   event purchaseCreated(uint indexed _bidId);
   
   //function  to save purchase details to Blockchain
   function savePurchase(string memory users, string memory iid, string memory pdate, string memory cd) public {
      purchaseList[purchaseCount] = purchase(users, iid, pdate, cd);
      emit purchaseCreated(purchaseCount);
      purchaseCount++;
    }

     //get purchase count
    function getPurchaseCount()  public view returns (uint) {
          return  purchaseCount;
    }

    function updateClaim(uint i, string memory value) public { 
      purchaseList[i].claim_details = value;
   }

    function getUsername(uint i) public view returns (string memory) {
        user memory doc = userList[i];
	return doc.username;
    }

    function getPassword(uint i) public view returns (string memory) {
        user memory doc = userList[i];
	return doc.password;
    }

    function getPhone(uint i) public view returns (string memory) {
        user memory doc = userList[i];
	return doc.phone;
    }    

    function getEmail(uint i) public view returns (string memory) {
        user memory doc = userList[i];
	return doc.email;
    }

    function getAddress(uint i) public view returns (string memory) {
        user memory doc = userList[i];
	return doc.user_address;
    }

    function getPolicyID(uint i) public view returns (string memory) {
        policy memory doc = policyList[i];
	return doc.policy_id;
    }

    function getPolicyName(uint i) public view returns (string memory) {
        policy memory doc = policyList[i];
	return doc.policy_name;
    }

    function getInsuredAmount(uint i) public view returns (string memory) {
        policy memory doc = policyList[i];
	return doc.insurance_amount;
    }

    function getPurchaseAmount(uint i) public view returns (string memory) {
        policy memory doc = policyList[i];
	return doc.purchase_amount;
    }

    function getDuration(uint i) public view returns (string memory) {
        policy memory doc = policyList[i];
	return doc.covered_duration;
    }
    
    function getDescription(uint i) public view returns (string memory) {
        policy memory doc = policyList[i];
	return doc.description;
    }

    function getProviderName(uint i) public view returns (string memory) {
        policy memory doc = policyList[i];
	return doc.provider_name;
    }

    function getPurchaserName(uint i) public view returns (string memory) {
       purchase memory doc = purchaseList[i];
       return doc.username;
    }

    function getInsuranceID(uint i) public view returns (string memory) {
        purchase memory doc = purchaseList[i];
	return doc.insurance_id;
    }

    function getPurchaseDate(uint i) public view returns (string memory) {
        purchase memory doc = purchaseList[i];
	return doc.purchase_date;
    }

    function getClaimDetails(uint i) public view returns (string memory) {
        purchase memory doc = purchaseList[i];
	return doc.claim_details;
    }
    
    
}