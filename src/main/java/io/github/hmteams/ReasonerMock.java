package io.github.hmteams;

import java.util.Collections;
import java.util.List;
import java.util.Random;
import java.util.concurrent.ThreadLocalRandom;
import java.util.logging.Logger;

import io.opentelemetry.api.GlobalOpenTelemetry;
import io.opentelemetry.api.trace.Span;
import io.opentelemetry.api.trace.StatusCode;
import io.opentelemetry.api.trace.Tracer;
import io.opentelemetry.context.Context;
import io.opentelemetry.context.Scope;

public class ReasonerMock {

  private Logger logger = Logger.getLogger(ReasonerMock.class.getName());

  // Get a Tracer instance from OpenTelemetry.
  Tracer tracer = GlobalOpenTelemetry.getTracer(ReasonerMock.class.getName(),
      "0.1.0");

  public static void main(String[] args) {
    ReasonerMock reasoner = new ReasonerMock();
    for (int i = 0; i < 1000; i++) {
      reasoner.reasoningCycle();
    }
    // createSpan();
  }

  private void reasoningCycle() {

    Span span = tracer.spanBuilder("reasoning_cycle").startSpan();
    // Make this new span the current active span.
    Scope scope = span.makeCurrent();
    // Start Traces
    goalRevision();
    planRevision();
    intentionProgression();

    scope.close();
    span.end();
  }

  private void goalRevision() {
    // Start a new span with the name "mySpan".
    Span span = tracer.spanBuilder("goal_revision").startSpan();
    // Make this new span the current active span.
    Scope scope = span.makeCurrent();

    try {

      span.setAttribute("xag.trigger.type", "event");
      span.setAttribute("xag.trigger.name", "ReviewGoals");
      span.setAttribute("xag.trigger.data", "[]");
      span.setAttribute("xag.query.goals.active", "[GetCoffee]");
      span.setAttribute("xag.query.goals.adopted", "[]");
      sleep();
    } catch (Exception e) {
      span.setStatus(StatusCode.ERROR, "Exception thrown in method");
    } finally {
      scope.close();
      span.end();
    }

  }

  private void planRevision() {
    List<String> PLANS = List.of("KitchenCoffee", "ShopCoffee", "OfficeCoffee");
    // Start a new span with the name "mySpan".
    Span span = tracer.spanBuilder("plan_revision").startSpan();
    // Make this new span the current active span.
    Scope scope = span.makeCurrent();

    Random rnd = new Random();
    try {

      span.setAttribute("xag.trigger.type", "event");
      span.setAttribute("xag.trigger.name", "ReviewPlans");
      span.setAttribute("xag.trigger.data", "[]");
      span.setAttribute("xag.query.applicablePlans", "[" + PLANS.get(rnd.nextInt(PLANS.size())) + "]");
      span.setAttribute("xag.query.staffCardAvailable", rnd.nextBoolean());
      span.setAttribute("xag.query.annInOffice", rnd.nextBoolean());
      span.setAttribute("xag.query.haveMoney", rnd.nextBoolean());
      sleep();
    } catch (Exception e) {
      span.setStatus(StatusCode.ERROR, "Exception thrown in method");
    } finally {
      scope.close();
      span.end();
    }

  }

  private void sleep() throws InterruptedException {
    Thread.sleep(ThreadLocalRandom.current().nextInt(150, 300));
  }

  private void intentionProgression() {
    Span span = tracer.spanBuilder("intention_progression").startSpan();
    // Make this new span the current active span.
    Scope scope = span.makeCurrent();

    try {

      span.setAttribute("xag.trigger.type", "event");
      span.setAttribute("xag.trigger.name", "ProgessIntentions");
      span.setAttribute("xag.trigger.data", "[]");
      sleep();
    } catch (Exception e) {
      span.setStatus(StatusCode.ERROR, "Exception thrown in method");
    } finally {
      scope.close();
      span.end();
    }

  }

  private static void createSpan() {
    // Get a Tracer instance from OpenTelemetry.
    Tracer tracer = GlobalOpenTelemetry.getTracer(ReasonerMock.class.getName(), "0.1.0");
    System.out.print("Entering method");

    // Start a new span with the name "mySpan".
    Span span = tracer.spanBuilder("xag").startSpan();

    // Make this new span the current active span.
    Scope scope = span.makeCurrent();

    // Close the scope to end it.
    scope.close();

    // Simulate an exception in the execution of the methods
    Throwable throwable = null;

    // If an exception was thrown during the method's execution, set the span's
    // status to ERROR.
    if (throwable != null) {
      span.setStatus(StatusCode.ERROR, "Exception thrown in method");
    } else {
      // If no exception was thrown, set a custom attribute "wordCount" on the span.
      span.setAttribute("query.coffee.quality", "BAD");
      span.setAttribute("query.coffee.cost", "NONE");
      span.setAttribute("query.staff_card", false);
      span.setAttribute("criteria.type", "uss");
      span.setAttribute("criteria.value", "uss.1-ac.1");
    }

    // End the span. This makes it ready to be exported to the configured exporter
    // (e.g., Jaeger, Zipkin).
    span.end();
  }

  // private static void reasonerReceivesGoalsReviewed() {
  //
  // }
  //
  // private static void reasonerReceivesPlansReviewed() {
  //
  // }
  //
  // private static void reasonerReceivesIntentionsProgressed() {
  //
  // }

  // private static void reasonerReceivesGoalsReviewed() {
  //
  // }
  //
  // private static void reasonerReceivesPlansReviewed() {
  //
  // }
  //
  // private static void reasonerReceivesIntentionsProgressed() {
  //
  // }

}
