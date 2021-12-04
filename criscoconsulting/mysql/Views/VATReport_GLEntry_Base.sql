
DELIMITER //
DROP VIEW  IF EXISTS `VATReport_GLEntry_Base`//
CREATE 
    ALGORITHM = UNDEFINED 
    DEFINER = `avuadmin`@`%` 
    SQL SECURITY DEFINER
VIEW `VATReport_GLEntry_Base` AS
    SELECT 
        `TGL`.`posting_date` AS `posting_date`,
        `TGL`.`name` AS `name`,
        `TGL`.`cost_center` AS `cost_center_GL`,
        `TSI`.`customer_name` AS `customer_name`,
        `TC`.`name` AS `customer_name_master`,
        CASE
            WHEN `TSI`.`tax_id` IS NULL = 1 THEN `TC`.`tax_id`
            ELSE `TSI`.`tax_id`
        END AS `Customer_VATNo`,
        `TPI`.`supplier_name` AS `supplier_name`,
        `TS`.`tax_id` AS `supplier_vat_number`,
        `TGL`.`docstatus` AS `docstatus`,
        IF(`TGL`.`voucher_type`='Sales Invoice' and `TSI`.`is_return`=1,
            'Sales Invoice Return',
            IF(`TGL`.`voucher_type`='Purchase Invoice' and `TPI`.`is_return`=1,
                'Purchase Invoice Return',
                `TGL`.`voucher_type`)) AS `sub_voucher_type`,
        `TGL`.`voucher_type` AS `voucher_type`,
        `TGL`.`voucher_no` AS `voucher_no`,
        `TGL`.`company` AS `company`,
        `TGL`.`is_advance` AS `is_advance`,
        `TGL`.`account` AS `account`,
        `TGL`.`debit` AS `debit`,
        `TGL`.`credit` AS `credit`,
        -- (CASE
        --     WHEN `TGL`.`debit` = 0 THEN `TGL`.`credit`
        --     ELSE `TGL`.`debit`
        -- END) * 100 / 5 AS `Amount`,
        IF(`TGL`.`voucher_type`='Purchase Invoice',
            `TPI`.`net_total` * (IF(`TPI`.`is_return`=1, -1, 1)),
            IF(`TGL`.`voucher_type`='Sales Invoice',
                `TSI`.`net_total` * (IF(`TSI`.`is_return`=1, -1, 1)),
                IF(`TGL`.`voucher_type`='Journal Entry',
                    `JE`.`total_debit` - `TGL`.`debit` - `TGL`.`credit`,
                    0)
            )
        ) AS `Amount`,
        CASE
            WHEN `TGL`.`debit` = 0 THEN - 1 * `TGL`.`credit`
            ELSE `TGL`.`debit`
        END AS `VAT_Amount`
    FROM `tabGL Entry` `TGL`
        LEFT JOIN `tabSales Invoice` `TSI` ON `TGL`.`voucher_no` = `TSI`.`name`
        LEFT JOIN `tabPurchase Invoice` `TPI` ON `TGL`.`voucher_no` = `TPI`.`name`
        LEFT JOIN `tabJournal Entry` AS `JE` ON `TGL`.`voucher_no` = `JE`.`name`
        LEFT JOIN `tabCustomer` `TC` ON `TSI`.`customer_name` = `TC`.`name`
        LEFT JOIN `tabSupplier` `TS` ON `TPI`.`supplier_name` = `TS`.`supplier_name`
    WHERE
        `TGL`.`docstatus` = 1
        AND (`TGL`.`account` LIKE '%VAT%'
            OR `TGL`.`account` LIKE '%ضريبة القيمة المضافة%')//

DELIMITER ;