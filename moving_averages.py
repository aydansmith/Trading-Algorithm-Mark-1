import quantopian.algorithm as algo
from quantopian.pipeline import Pipeline
from quantopian.pipeline.data.builtin import USEquityPricing
from quantopian.pipeline.filters import QTradableStocksUS
from zipline.pipeline.factors import SimpleMovingAverage


def initialize(context):
    """
    Called once at the start of the algorithm.
    """
    context.security = sid(24)
    
    # Rebalance every day, 1 hour after market open.
    algo.schedule_function(
        rebalance,
        algo.date_rules.every_day(),
        algo.time_rules.market_open(hours=1),
    )

def rebalance(context, data):
    """
    Execute orders according to our schedule_function() timing.
    """
    past_price_data = data.history(
        context.security,
        fields='price',
        bar_count=5,
        frequency='1d'
    )
    
    average_five_day = past_price_data.mean()
    
    past_price_data_two = data.history(
        context.security,
        fields='price',
        bar_count=20,
        frequency='1d'
    )
    
    average_twenty_day = past_price_data_two.mean()
    
    if data.can_trade(context.security):
        if average_five_day > average_twenty_day:
            algo.order_target_percent(context.security, 1)
            log.info("Buying %s" % (context.security.symbol))
    
        elif average_five_day < average_twenty_day:
            algo.order_target_percent(context.security, 0)
            log.info("Selling %s" % (context.security.symbol))
