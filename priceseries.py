import math

class PriceSeries:
    """
    Représentation d'une série temporelle de prix financiers.
    
    Attributes:
        values: Liste de prix indexés par le temps
        name: Identifiant de la série
    
    Class Attributes:
        TRADING_DAYS_PER_YEAR: Constante d'annualisation 
        (convention US equities, peut varier selon l'actif)
    """
    
    TRADING_DAYS_PER_YEAR: int = 252
    
    def __init__(self, values: list[float], name: str = "unnamed") -> None:
        self.values = list(values)  # Copie défensive
        self.name = name
    
    def __repr__(self) -> str:
        return f"PriceSeries({self.name!r}, {len(self.values)} values)"
    
    def __str__(self) -> str:
        if self.values:
            return f"{self.name}: {self.values[-1]:.2f} (latest)"
        return f"{self.name}: empty"
    
    def __len__(self) -> int:
        return len(self.values)
    def linear_return(self, t: int) -> float:
        """Rendement linéaire (arithmétique) entre t-1 et t."""
        return (self.values[t] - self.values[t-1]) / self.values[t-1]
    
    def log_return(self, t: int) -> float:
        """Log-rendement entre t-1 et t."""
        return math.log(self.values[t] / self.values[t-1])
    
    @property
    def total_return(self) -> float:
        """Rendement total sur toute la période."""
        if len(self.values) < 2:
            return 0.0
        return (self.values[-1] - self.values[0]) / self.values[0]

    def get_all_linear_returns(self) -> list[float]:
     """Retourne la liste de tous les rendements linéaires."""
     return [self.linear_return(t) for t in range(1, len(self.values))]

    def get_all_log_returns(self) -> list[float]:
        """Retourne la liste de tous les log-rendements."""
        return [self.log_return(t) for t in range(1, len(self.values))]
    def annualized_volatility(self) -> float:
        if len(self.values) < 3:
                raise ValueError("Not enough data points")
                
        log_returns = self.get_all_log_returns()
        n = len(log_returns)
        mean = sum(log_returns) / n
        var = sum((l_r - mean)**2 for l_r in log_returns) / (n - 1)
        daily_vol = math.sqrt(var)

        return daily_vol * math.sqrt(self.TRADING_DAYS_PER_YEAR)

    def annualized_return(self) -> float:
        """
        Retourne le rendement annualisé sur toute la période.
        """
        if len(self) < 2:
            raise ValueError("Not enough data points")
        r = self.get_all_log_returns()
        return (sum(r) / len(r)) * self.TRADING_DAYS_PER_YEAR

    def sharpe_ratio(self, risk_free_rate: float = 0.0) -> float:
        """
        Ratio de sharpe annualisé : 
            - ratio entre les rendements esperés d'une stratégie et sa vol
            - rendement par unité de risque
        
        Formule: SR = (μ - r_f) / σ
        
        Args:
            risk_free_rate: taux sans risque annuel
        
        """
        vol = self.annualized_volatility()
        if vol == 0:
            return 0.0
        excess_return = self.annualized_return() - risk_free_rate
        return excess_return / vol
    def drawdown_at(self, t: int) -> float:
     """Drawdown au temps t."""
     if t < 0 or t >= len(self.values):
        raise IndexError(f"index {t} is out of range for series of length {len(self.values)}")

     peak = max(self.values[:t+1])
     if peak == 0:
        return 0.0
     return (self.values[t] - peak) / peak

def max_drawdown(self) -> float:
    """Drawdown maximum sur toute la série."""
    max_dd = 0.0
    peak = self.values[0]

    for value in self.values[1:]:
        peak = max(peak, value)
        if peak > 0:
            dd = (value - peak) / peak
            max_dd = min(max_dd, dd)

    return max_dd
