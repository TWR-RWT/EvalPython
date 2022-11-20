select 
a.id_contrat, -- 0
a.id_location, -- 1
a.id_locataire, -- 2
a.agence, -- 3
a.frais_agence, -- 4
a.date_debut, -- 5
a.depot_garantie, -- 6
a.date_etat_des_lieux, -- 7
a.montant_etat_des_lieux, -- 8
a.date_fin, -- 9
a.loyer, -- 10
a.charges, -- 11
coalesce(sum(b.montant) filter(where lower(b.paiement_type)='loyer'), 0) as montantLoyer, -- 12
coalesce(sum(b.montant) filter(where lower(b.paiement_type)='charges'), 0) as montantCharges, -- 13
coalesce(sum(b.montant) filter(where lower(b.paiement_type)='depot_garantie'), 0) as montantDP, -- 14

CASE WHEN a.date_fin IS NULL THEN
EXTRACT(YEAR FROM age(a.date_debut))*12 + EXTRACT(MONTH FROM age(a.date_debut))
ELSE 
EXTRACT(YEAR FROM age(a.date_fin, a.date_debut))*12 + EXTRACT(MONTH FROM age(a.date_fin, a.date_debut)) + EXTRACT(DAY FROM age(a.date_fin, a.date_debut))/30
END as duree, -- 15

(CASE WHEN a.date_fin IS NULL THEN
EXTRACT(YEAR FROM age(a.date_debut))*12 + EXTRACT(MONTH FROM age(a.date_debut))
ELSE 
EXTRACT(YEAR FROM age(a.date_fin, a.date_debut))*12 + EXTRACT(MONTH FROM age(a.date_fin, a.date_debut)) + EXTRACT(DAY FROM age(a.date_fin, a.date_debut))/30
END) * a.loyer - coalesce(sum(b.montant) filter(where lower(b.paiement_type)='loyer'), 0) 
as loyertotal, -- 16

(CASE WHEN a.date_fin IS NULL THEN
EXTRACT(YEAR FROM age(a.date_debut))*12 + EXTRACT(MONTH FROM age(a.date_debut))
ELSE 
EXTRACT(YEAR FROM age(a.date_fin, a.date_debut))*12 + EXTRACT(MONTH FROM age(a.date_fin, a.date_debut)) + EXTRACT(DAY FROM age(a.date_fin, a.date_debut))/30
END) * a.charges - coalesce(sum(b.montant) filter(where lower(b.paiement_type)='charges'), 0) 
as chargestotal, -- 17

ROUND(((CASE WHEN a.date_fin IS NULL THEN
EXTRACT(YEAR FROM age(a.date_debut))*12 + EXTRACT(MONTH FROM age(a.date_debut))
ELSE 
EXTRACT(YEAR FROM age(a.date_fin, a.date_debut))*12 + EXTRACT(MONTH FROM age(a.date_fin, a.date_debut)) + EXTRACT(DAY FROM age(a.date_fin, a.date_debut))/30
END) * a.loyer - coalesce(sum(b.montant) filter(where lower(b.paiement_type)='loyer'), 0)) 
+
((CASE WHEN a.date_fin IS NULL THEN
EXTRACT(YEAR FROM age(a.date_debut))*12 + EXTRACT(MONTH FROM age(a.date_debut))
ELSE 
EXTRACT(YEAR FROM age(a.date_fin, a.date_debut))*12 + EXTRACT(MONTH FROM age(a.date_fin, a.date_debut)) + EXTRACT(DAY FROM age(a.date_fin, a.date_debut))/30
END) * a.charges - coalesce(sum(b.montant) filter(where lower(b.paiement_type)='charges'), 0)),2) 
as ArriereLoyerCharges, -- 18

ROUND(a.depot_garantie - coalesce(sum(b.montant) filter(where lower(b.paiement_type)='depot de garantie'), 0),2) 
as ArriereDepotGarantie, -- 19

ROUND(((CASE WHEN a.date_fin IS NULL THEN
EXTRACT(YEAR FROM age(a.date_debut))*12 + EXTRACT(MONTH FROM age(a.date_debut))
ELSE 
EXTRACT(YEAR FROM age(a.date_fin, a.date_debut))*12 + EXTRACT(MONTH FROM age(a.date_fin, a.date_debut)) + EXTRACT(DAY FROM age(a.date_fin, a.date_debut))/30
END) * a.loyer - coalesce(sum(b.montant) filter(where lower(b.paiement_type)='loyer'), 0))
* (a.frais_agence/100), 2)
as lfraisagenceloyer -- 20


from immo.contrats_loc as a
left join immo.paiements as b 
on (a.id_contrat = b.id_contrat)
group by a.id_contrat 
order by a.id_contrat