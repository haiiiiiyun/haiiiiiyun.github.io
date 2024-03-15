---
title: One-to-one, one-to-many, many-to-many relationship in Database
date: 2024-03-07
tags: db
categoris: Programming
---

## One-to-one relation

One record of the first table will be linked to zero or one record of another table. For example, each employee in the `Employee` table will have a corresponding row in `EmployeeDetails` table.

```
Employee          EmployeeDetails
  EmployeeID         EmployeeID
  Name,...           Detail,...
```

Each employee has none or just one corresponding record in `EmployeeDetails`.

## One-to-many relation

One-to-many is the most commonly used relationship among tables. A single record from one table can be linked to zero or more rows in another table.

For example, each employee has zero or more records of address.

The `Employee` and `Address` tables are linked by the key column EmployeeID. It is a foreign key in the `Address` table linking to the primary key EmployeeID in the `Employee` table. Thus, one record of the `Employee` table can point to multiple records in the `Address` table. This is a One-to-Many relationship.

```
Employee          Address
  EmployeeID         ForeignKey(EmployeeID)
  Name,...           Detail,...
```

## Many-to-many relation

Many-to-Many relationship lets us relate each row in one table to many rows in another table and vice versa.

As an example, an employee in the `Employee` table can have many skills from the `EmployeeSkill` table and also, one skill can be associated with one or more employees.

```
Employee          EmployeeSkill                Skill
  EmployeeID         ForeignKey(EmployeeID)        SkillID
  Name,...           ForeignKey(SkillID)           Description,...
```

The many-to-many relation between `Employee` and `Skill` using the junction table `EmploySkill`.

 Individually, the `Employee` and `EmployeeSkill` have a one-to-many relation, and the `Skill` and `EmployeeSkill` tables have one-to-many relation. But, they form many-to-many relation by using a junction table `EmployeeSkill`.

See https://www.tutorialsteacher.com/sqlserver/tables-relations