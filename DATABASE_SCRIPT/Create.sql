IF EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID('Booking') AND type in (N'U'))
    DROP TABLE Booking
GO 

IF EXISTS ( SELECT * FROM sys.objects WHERE object_id = OBJECT_ID('UserOfLicense') AND type in (N'U'))
    DROP TABLE UserOfLicense
GO

IF EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID('Users') AND type in (N'U'))
    DROP TABLE User
GO

IF EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID('MenuItemCategories') AND type in (N'U'))