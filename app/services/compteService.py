from sqlalchemy.orm import Session
from app.models.compte import Compte
from app.models.ticket import Ticket

class CompteService:
    @staticmethod
    def creer_compte(db: Session, numero_compte: str, solde_initial: float = 10.0):
        """
        Crée un compte avec un numéro et un solde initial
        """
        try:
            # Création d'un nouveau compte
            nouveau_compte = Compte(
                numero_compte=numero_compte,
                solde=solde_initial
            )
            
            # Ajout du compte dans la base de données
            db.add(nouveau_compte)
            db.commit()
            db.refresh(nouveau_compte)

            return {"message": "Compte créé avec succès", "compte": nouveau_compte}

        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def effectuer_paiement(db: Session, numero_compte: str, ticket_id: int):
        """
        Effectue un paiement en fonction du ticket et du compte
        """
        try:
            # Récupération du compte en fonction du numéro de compte
            compte = db.query(Compte).filter(Compte.numero_compte == numero_compte).first()

            if not compte:
                return {"error": "Compte introuvable"}
            
            # Récupération du ticket en fonction de l'ID
            ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()

            if not ticket:
                return {"error": "Ticket introuvable"}
            
            # Calcul du montant total (prix * quantité)
            montant_total = ticket.price * ticket.qte

            # Vérification si le solde du compte est suffisant
            if compte.solde < montant_total:
                return {"error": "Solde insuffisant pour effectuer le paiement"}
            
            # Déduction du montant du ticket du solde du compte
            compte.solde -= montant_total
            db.commit()
            db.refresh(compte)

            return {"message": f"Paiement effectué avec succès. Nouveau solde: {compte.solde}", "compte": compte}
        
        except Exception as e:
            return {"error": str(e)}
