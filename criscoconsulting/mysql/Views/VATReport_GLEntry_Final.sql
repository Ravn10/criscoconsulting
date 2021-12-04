DELIMITER //


DROP VIEW  IF EXISTS `VATReport_GLEntry_Final`//
CREATE 
    ALGORITHM = UNDEFINED 
    DEFINER = `avuadmin`@`%` 
    SQL SECURITY DEFINER
VIEW`VATReport_GLEntry_Final` AS
    SELECT 
        `VB`.`posting_date` AS `01#Posting Date:Date:100`,
        'Credit' AS `02#Type`,
        `VB`.`sub_voucher_type` AS `03#Voucher Type::100`,
        `VB`.`voucher_type` AS `04#voucher_type:.:100`,
        `VB`.`voucher_no` AS `04#Voucher No:Dynamic Link/voucher_type:150`,
        `VB`.`company` AS `05#Company`,
        `VB`.`account` AS `06#Account:Link/Account:100`,
        `VB`.`customer_name` AS `07#Customer Name::200`,
        `VB`.`Customer_VATNo` AS `08#Customer VAT No::150`,
        `VB`.`Supplier_name` AS `09#Supplier Name::200`,
        `VB`.`supplier_vat_number` AS `10#Supplier VAT No::150`,
        IF(`VB`.`credit` = 0, 0, `VB`.`Amount`) AS `11#Sales Amount (Credit)@Currency:Float:150`,
        CAST(`VB`.`credit` AS DECIMAL (18 , 2 )) AS `12#VAT Credit (Sales)@Currency:Float:130`,
        IF(`VB`.`debit` = 0, 0, `VB`.`Amount`) AS `13#Purchase Amount (Debit)@Currency:Float:180`,
        CAST(`VB`.`debit` AS DECIMAL (18 , 2 )) AS `14#VAT Debit (Purchase)@Currency:Float:130`
    FROM
       `VATReport_GLEntry_Base` `VB`
    WHERE
        `VB`.`credit` > 0 
    UNION SELECT 
        `VB`.`posting_date` AS `posting_date`,
        'Debit' AS `Type`,
        `VB`.`sub_voucher_type`,
        `VB`.`voucher_type` AS `voucher_type`,
        `VB`.`voucher_no` AS `voucher_no`,
        `VB`.`company` AS `company`,
        `VB`.`account` AS `account`,
        `VB`.`customer_name` AS `07#Customer Name::200`,
        `VB`.`Customer_VATNo` AS `08#Customer VAT No::150`,
        `VB`.`Supplier_name` AS `supplier_name`,
        `VB`.`supplier_vat_number` AS `supplier_vat_number`,
        IF(`VB`.`credit` = 0, 0, `VB`.`Amount`) AS `credit`,
        CAST(`VB`.`credit` AS DECIMAL (18 , 2 )) AS `VAT`,
        IF(`VB`.`debit` = 0, 0, `VB`.`Amount`) AS `debit`,
        CAST(`VB`.`debit` AS DECIMAL (18 , 2 )) AS `VAT`
    FROM
        `VATReport_GLEntry_Base` `VB`
    WHERE
        `VB`.`debit` > 0//


DELIMITER ;