
create database sap_projem
go
use sap_projem
create table yonetim_sureci(proje_id smallint identity(1,1) primary key ,proje_adi nvarchar(80) ,tahmin_butce money , tamamlanan tinyint , harcanan money, sure smallint ,beklenen smallint, verimlilik tinyint)
go

alter table yonetim_sureci alter column tamamlanan int
alter table yonetim_sureci alter column sure int
alter table yonetim_sureci alter column beklenen int
alter table yonetim_sureci alter column butce_verim int

alter table yonetim_sureci add sure_verim int
create table kullanici (kullanici_ad nvarchar(120), sifre nvarchar(40), posta nvarchar(120))
alter table kullanici add usr_id int identity(1,1) primary key
alter table yonetim_sureci add kullanici int foreign key references kullanici(usr_id)
create table yonetici(yntc_id int identity(1,1) primary key,yonetici_ad nvarchar(120), sifre nvarchar(40), posta nvarchar(120))
alter table yonetim_sureci add yonetici int foreign key references yonetici(yntc_id)

alter table yonetim_sureci alter column tahmin_butce float
alter table yonetim_sureci alter column harcanan float
alter table yonetim_sureci alter column butce_verim float
alter table yonetim_sureci alter column sure_verim float
alter table yonetim_sureci alter column sure float
alter table yonetim_sureci alter column beklenen float

