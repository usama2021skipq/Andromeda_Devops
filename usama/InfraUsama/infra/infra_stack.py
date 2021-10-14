# For consistency with other languages, `cdk` is the preferred import name for
# the CDK's core module.  The following line also imports it as `core` for use
# with examples from the CDK Developer's Guide, which are in the process of
# being updated to use `cdk`.  You may delete this import if you don't need it.

from aws_cdk import core as cdk
from aws_cdk import core
from aws_cdk import aws_lambda as lambda_
from aws_cdk import aws_events
from aws_cdk import aws_events_targets



class InfraStackUsama(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here
        # hw_lambda = self.create_lambda('AndromedaLambda', './lambda', 'handler.lambda_handler')
        web_health_lambda = self.create_lambda('AndromedaLambda', './lambda', 'web_health_publisher.health_monitor')
        # lambda_schedule = aws_events.Schedule.rate(core.Duration.minutes(5))
        # target_lambda = aws_events_targets.LambdaFunction(web_health_lambda)
        # Run_Rule = aws_events.Rule(self, 'AndromedaLambdaPeriodic', schedule = lambda_schedule, targets = [target_lambda])
        self.periodic_lambda("AndromedaLambdaPeriodic", 5, web_health_lambda)
        
    
    def create_lambda(self, id, asset, handler):
        return lambda_.Function(self, id,
        code=lambda_.Code.asset(asset),
        handler=handler,
        runtime=lambda_.Runtime.PYTHON_3_6)
        
    
    def periodic_lambda(self, id, duration_in_minutes, lambda_fun,):
        lambda_schedule = aws_events.Schedule.rate(core.Duration.minutes(duration_in_minutes))
        target_lambda = aws_events_targets.LambdaFunction(lambda_fun)
        Rule = aws_events.Rule(self, id, schedule = lambda_schedule, targets = [target_lambda])