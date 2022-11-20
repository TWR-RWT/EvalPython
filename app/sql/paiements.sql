with 
_base as (
select 
a.id_contrat, -- 0
a.id_location, -- 1
a.id_locataire, -- 2

coalesce(sum(b.montant) filter(where lower(b.paiement_type)='loyer'), 0) as montantLoyer, -- 12
coalesce(sum(b.montant) filter(where lower(b.paiement_type)='charges'), 0) as montantCharges, -- 13
coalesce(sum(b.montant) filter(where lower(b.paiement_type)='depot_garantie'), 0) as montantDP, -- 14

ROUND(CASE WHEN a.date_fin IS NULL THEN
EXTRACT(YEAR FROM age(a.date_debut))*12 + EXTRACT(MONTH FROM age(a.date_debut))
ELSE 
EXTRACT(YEAR FROM age(a.date_fin, a.date_debut))*12 + EXTRACT(MONTH FROM age(a.date_fin, a.date_debut)) + EXTRACT(DAY FROM age(a.date_fin, a.date_debut))/30
END, 2) as duree, -- 15

ROUND((CASE WHEN a.date_fin IS NULL THEN
EXTRACT(YEAR FROM age(a.date_debut))*12 + EXTRACT(MONTH FROM age(a.date_debut))
ELSE 
EXTRACT(YEAR FROM age(a.date_fin, a.date_debut))*12 + EXTRACT(MONTH FROM age(a.date_fin, a.date_debut)) + EXTRACT(DAY FROM age(a.date_fin, a.date_debut))/30
END) 
* a.loyer * (1 + a.frais_agence/100)
- coalesce(sum(b.montant) filter(where lower(b.paiement_type)='loyer'), 0), 2)
as loyertotal, -- 16 avec frais agence

ROUND((CASE WHEN a.date_fin IS NULL THEN
EXTRACT(YEAR FROM age(a.date_debut))*12 + EXTRACT(MONTH FROM age(a.date_debut))
ELSE 
EXTRACT(YEAR FROM age(a.date_fin, a.date_debut))*12 + EXTRACT(MONTH FROM age(a.date_fin, a.date_debut)) + EXTRACT(DAY FROM age(a.date_fin, a.date_debut))/30
END) * a.charges - coalesce(sum(b.montant) filter(where lower(b.paiement_type)='charges'), 0), 2)
as chargestotal, -- 17

ROUND(((CASE WHEN a.date_fin IS NULL THEN
EXTRACT(YEAR FROM age(a.date_debut))*12 + EXTRACT(MONTH FROM age(a.date_debut))
ELSE 
EXTRACT(YEAR FROM age(a.date_fin, a.date_debut))*12 + EXTRACT(MONTH FROM age(a.date_fin, a.date_debut)) + EXTRACT(DAY FROM age(a.date_fin, a.date_debut))/30
END) 
* a.loyer * (1 + a.frais_agence/100)
- coalesce(sum(b.montant) filter(where lower(b.paiement_type)='loyer'), 0)) 
+
((CASE WHEN a.date_fin IS NULL THEN
EXTRACT(YEAR FROM age(a.date_debut))*12 + EXTRACT(MONTH FROM age(a.date_debut))
ELSE 
EXTRACT(YEAR FROM age(a.date_fin, a.date_debut))*12 + EXTRACT(MONTH FROM age(a.date_fin, a.date_debut)) + EXTRACT(DAY FROM age(a.date_fin, a.date_debut))/30
END) * a.charges - coalesce(sum(b.montant) filter(where lower(b.paiement_type)='charges'), 0)),2) 
as ArriereLoyerCharges, -- 18 avec frais agence

ROUND(a.depot_garantie - coalesce(sum(b.montant) filter(where lower(b.paiement_type)='depot de garantie'), 0),2) 
as ArriereDepotGarantie, -- 19

ROUND(((CASE WHEN a.date_fin IS NULL THEN
EXTRACT(YEAR FROM age(a.date_debut))*12 + EXTRACT(MONTH FROM age(a.date_debut))
ELSE 
EXTRACT(YEAR FROM age(a.date_fin, a.date_debut))*12 + EXTRACT(MONTH FROM age(a.date_fin, a.date_debut)) + EXTRACT(DAY FROM age(a.date_fin, a.date_debut))/30
END) * a.loyer - coalesce(sum(b.montant) filter(where lower(b.paiement_type)='loyer'), 0))
* (a.frais_agence/100), 2)
as fraisagenceloyer, -- 20 frais agence

a.date_debut + interval '1 month' 
* ROUND(coalesce(sum(b.montant) filter(where lower(b.paiement_type)='loyer'), 0) / (a.Loyer * (1 + a.frais_agence/100))) 
+ interval '1 day'
* FLOOR((ROUND(coalesce(sum(b.montant) filter(where lower(b.paiement_type)='loyer'), 0) / (a.Loyer * (1 + a.frais_agence/100)), 2)
- ROUND(coalesce(sum(b.montant) filter(where lower(b.paiement_type)='loyer'), 0) / (a.Loyer * (1 + a.frais_agence/100))))
*30)
as date_max_quittance -- 21

from immo.contrats_loc as a
left join immo.paiements as b 
on (a.id_contrat = b.id_contrat)
group by a.id_contrat 
order by a.id_contrat)

select 
t2.id_paiement as paiement, -- 0
t1.id_contrat as id_contrat, -- 1
t2.date_paiement as date_paiement, -- 2
t2.paiement_type as paiement_type, -- 3
t2.complement as complement_paiement, -- 4
t2.montant as montant, -- 5
t3.id_locataire as id_locataire, -- 6
t3.nom as nom, -- 7
t3.prenom as prenom, -- 8
t3.adresse as adresse_locataire, -- 9
t3.code_postal as code_postal, -- 10
t3.ville as ville, -- 11
t3.telephone as telephone, -- 12
t3.email as email, -- 13
t4.id_location as id_location, -- 14
t4.adresse as adresse_location, -- 15
t4.complement as complement_location, -- 16
t4.code_postal as code_postal_location, -- 17
t4.ville as ville_location, -- 18
t1.agence as agence, -- 19
t1.frais_agence as frais_agence, -- 20
t1.date_debut as date_debut, -- 21
t1.depot_garantie as depot_garantie, -- 22
t1.date_etat_des_lieux as date_etat_des_lieux, -- 23
t1.montant_etat_des_lieux as montant_etat_des_lieux, -- 24
t1.date_fin as date_fin, -- 25
t1.loyer as loyer, -- 26
t1.charges as charges, -- 27
_base.montantLoyer as montantLoyer, -- 28
_base.montantCharges as montantCharges, -- 29
_base.montantDP as montantDP, -- 30
_base.duree as duree, -- 31
_base.loyertotal as loyertotal, -- 32 --- avec frais agence
_base.chargestotal as chargestotal, -- 33
_base.ArriereLoyerCharges as ArriereLoyerCharges, -- 34 avec frais agence
_base.ArriereDepotGarantie as ArriereDepotGarantie, -- 35
_base.fraisagenceloyer as fraisagenceloyer, -- 36
_base.date_max_quittance as date_max_quittance -- 37

from immo.contrats_loc as t1
inner join _base on (t1.id_contrat = _base.id_contrat)
inner join immo.paiements as t2 on (t1.id_contrat = t2.id_contrat)
inner join immo.locataires as t3 on (t1.id_locataire = t3.id_locataire)
inner join immo.locations as t4 on (t1.id_location = t4.id_location)
where t1.id_contrat = {0}