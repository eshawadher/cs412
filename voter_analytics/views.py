# File: voter_analytics/views.py
# Author: Esha Wadher (eshaaw@bu.edu), 03/20/2026
# Description:
# Contains the class-based views for the voter_analytics application.
# These views handle incoming HTTP requests, retrieve Voter data
# from the database, and render the appropriate templates.
# Includes a list view to display and filter registered voters in Newton, MA,

from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Voter

import plotly
import plotly.graph_objs as go


class VoterListView(ListView):
    """view to dipslay a list of voters"""

    template_name = "voter_analytics/voters.html"
    model = Voter
    context_object_name = "voters"
    paginate_by = 100

    def get_queryset(self):
        """return filtered queirsyet based on the paramters"""
        voters = super().get_queryset()
        if "party_affiliation" in self.request.GET:
            party = self.request.GET["party_affiliation"]
            if party:
                voters = voters.filter(party_affiliation=party)

        if "min_dob" in self.request.GET:
            min_dob = self.request.GET["min_dob"]
            if min_dob:
                voters = voters.filter(date_of_birth__year__gte=min_dob)

        if "max_dob" in self.request.GET:
            max_dob = self.request.GET["max_dob"]
            if max_dob:
                voters = voters.filter(date_of_birth__year__lte=max_dob)

        if "voter_score" in self.request.GET:
            voter_score = self.request.GET["voter_score"]
            if voter_score:
                voters = voters.filter(voter_score=voter_score)

        if "v20state" in self.request.GET:
            voters = voters.filter(v20state=True)

        if "v21town" in self.request.GET:
            voters = voters.filter(v21town=True)

        if "v21primary" in self.request.GET:
            voters = voters.filter(v21primary=True)

        if "v22general" in self.request.GET:
            voters = voters.filter(v22general=True)

        if "v23town" in self.request.GET:
            voters = voters.filter(v23town=True)

        return voters

    def get_context_data(self, **kwargs):
        """add extra context so the filter form keeps selected values"""
        context = super().get_context_data(**kwargs)

        context["party_choices"] = (
            Voter.objects.values_list("party_affiliation")
            .distinct()
            .order_by("party_affiliation")
        )

        context["year_choices"] = (
            Voter.objects.values_list("date_of_birth__year")
            .distinct()
            .order_by("date_of_birth__year")
        )
        context["score_choices"] = (
            Voter.objects.values_list("voter_score").distinct().order_by("voter_score")
        )

        context["selected_party"] = self.request.GET.get("party_affiliation", "")
        context["selected_min_dob"] = self.request.GET.get("min_dob", "")
        context["selected_max_dob"] = self.request.GET.get("max_dob", "")
        context["selected_voter_score"] = self.request.GET.get("voter_score", "")

        context["checked_v20state"] = "v20state" in self.request.GET
        context["checked_v21town"] = "v21town" in self.request.GET
        context["checked_v21primary"] = "v21primary" in self.request.GET
        context["checked_v22general"] = "v22general" in self.request.GET
        context["checked_v23town"] = "v23town" in self.request.GET

        return context


class VoterDetailView(DetailView):
    """View to show detail page for one voter."""

    template_name = "voter_analytics/voter_detail.html"
    model = Voter
    context_object_name = "voter"


class VoterGraphView(ListView):
    """View to display graphs of aggregate voter data."""

    template_name = "voter_analytics/graphs.html"
    model = Voter
    context_object_name = "voters"

    def get_queryset(self):
        """Return filtered queryset based on GET parameters."""
        voters = super().get_queryset()

        if "party_affiliation" in self.request.GET:
            party = self.request.GET["party_affiliation"]
            if party:
                voters = voters.filter(party_affiliation=party)

        if "min_dob" in self.request.GET:
            min_dob = self.request.GET["min_dob"]
            if min_dob:
                voters = voters.filter(date_of_birth__year__gte=min_dob)

        if "max_dob" in self.request.GET:
            max_dob = self.request.GET["max_dob"]
            if max_dob:
                voters = voters.filter(date_of_birth__year__lte=max_dob)

        if "voter_score" in self.request.GET:
            voter_score = self.request.GET["voter_score"]
            if voter_score:
                voters = voters.filter(voter_score=voter_score)

        if "v20state" in self.request.GET:
            voters = voters.filter(v20state=True)

        if "v21town" in self.request.GET:
            voters = voters.filter(v21town=True)

        if "v21primary" in self.request.GET:
            voters = voters.filter(v21primary=True)

        if "v22general" in self.request.GET:
            voters = voters.filter(v22general=True)

        if "v23town" in self.request.GET:
            voters = voters.filter(v23town=True)

        return voters

    def get_context_data(self, **kwargs):
        """Provide context variables including graphs for use in template."""
        context = super().get_context_data(**kwargs)
        voters = self.get_queryset()

        # Graphs
        birth_years = voters.values_list("date_of_birth__year")
        year_counts = {}
        for y in birth_years:
            year_counts[y] = year_counts.get(y, 0) + 1
        sorted_years = sorted(year_counts.keys())

        fig1 = go.Bar(
            x=sorted_years,
            y=[year_counts[y] for y in sorted_years],
        )
        graph_div_dob = plotly.offline.plot(
            {"data": [fig1], "layout_title_text": "Voters by Year of Birth"},
            auto_open=False,
            output_type="div",
        )
        context["graph_div_dob"] = graph_div_dob

        # --- Graph 2: Party affiliation pie chart ---
        party_counts = voters.values("party_affiliation").annotate(count=Count("id"))
        fig2 = go.Pie(
            labels=[p["party_affiliation"].strip() for p in party_counts],
            values=[p["count"] for p in party_counts],
        )
        graph_div_party = plotly.offline.plot(
            {"data": [fig2], "layout_title_text": "Voters by Party Affiliation"},
            auto_open=False,
            output_type="div",
        )
        context["graph_div_party"] = graph_div_party

        # --- Graph 3: Election participation histogram ---
        elections = ["v20state", "v21town", "v21primary", "v22general", "v23town"]
        election_counts = [voters.filter(**{e: True}).count() for e in elections]
        fig3 = go.Bar(
            x=elections,
            y=election_counts,
        )
        graph_div_elections = plotly.offline.plot(
            {"data": [fig3], "layout_title_text": "Voter Participation by Election"},
            auto_open=False,
            output_type="div",
        )
        context["graph_div_elections"] = graph_div_elections

        # filter options
        context["parties"] = (
            Voter.objects.values_list("party_affiliation", flat=True)
            .distinct()
            .order_by("party_affiliation")
        )
        context["years"] = list(range(1900, 2007))
        context["scores"] = list(range(0, 6))

        context["selected_party"] = self.request.GET.get("party_affiliation", "")
        context["selected_min_dob"] = self.request.GET.get("min_dob", "")
        context["selected_max_dob"] = self.request.GET.get("max_dob", "")
        context["selected_voter_score"] = self.request.GET.get("voter_score", "")
        context["selected_v20state"] = self.request.GET.get("v20state", "")
        context["selected_v21town"] = self.request.GET.get("v21town", "")
        context["selected_v21primary"] = self.request.GET.get("v21primary", "")
        context["selected_v22general"] = self.request.GET.get("v22general", "")
        context["selected_v23town"] = self.request.GET.get("v23town", "")

        return context


class GraphsView(ListView):
    """view to show graphs for voter data"""

    template_name = "voter_analytics/graphs.html"
    model = Voter
    context_object_name = "voters"

    def get_queryset(self):
        voters = super().get_queryset()

        if "party_affiliation" in self.request.GET:
            party_affiliation = self.request.GET["party_affiliation"]
            if party_affiliation:
                voters = voters.filter(party_affiliation=party_affiliation)

        if "min_dob" in self.request.GET:
            min_dob = self.request.GET["min_dob"]
            if min_dob:
                voters = voters.filter(date_of_birth__year__gte=min_dob)

        if "max_dob" in self.request.GET:
            max_dob = self.request.GET["max_dob"]
            if max_dob:
                voters = voters.filter(date_of_birth__year__lte=max_dob)

        if "voter_score" in self.request.GET:
            voter_score = self.request.GET["voter_score"]
            if voter_score:
                voters = voters.filter(voter_score=voter_score)

        if "v20state" in self.request.GET:
            voters = voters.filter(v20state=True)

        if "v21town" in self.request.GET:
            voters = voters.filter(v21town=True)

        if "v21primary" in self.request.GET:
            voters = voters.filter(v21primary=True)

        if "v22general" in self.request.GET:
            voters = voters.filter(v22general=True)

        if "v23town" in self.request.GET:
            voters = voters.filter(v23town=True)

        return voters

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        voters = self.get_queryset()

        context["party_choices"] = Voter.objects.values_list(
            "party_affiliation"
        ).distinct()
        context["year_choices"] = (
            Voter.objects.values_list("date_of_birth__year")
            .distinct()
            .order_by("date_of_birth__year")
        )
        context["score_choices"] = (
            Voter.objects.values_list("voter_score").distinct().order_by("voter_score")
        )

        context["selected_party_affiliation"] = self.request.GET.get(
            "party_affiliation", ""
        )
        context["selected_min_dob"] = self.request.GET.get("min_dob", "")
        context["selected_max_dob"] = self.request.GET.get("max_dob", "")
        context["selected_voter_score"] = self.request.GET.get("voter_score", "")

        context["checked_v20state"] = "v20state" in self.request.GET
        context["checked_v21town"] = "v21town" in self.request.GET
        context["checked_v21primary"] = "v21primary" in self.request.GET
        context["checked_v22general"] = "v22general" in self.request.GET
        context["checked_v23town"] = "v23town" in self.request.GET

        # graph 1: histogram of birth years
        x = []
        for v in voters:
            x.append(v.date_of_birth.year)

        fig = go.Histogram(x=x)
        graph_div_birth_years = plotly.offline.plot(
            {
                "data": [fig],
                "layout_title_text": "Distribution of Voters by Birth Year",
            },
            auto_open=False,
            output_type="div",
        )
        context["graph_div_birth_years"] = graph_div_birth_years

        # graph 2: pie chart of party affiliation
        parties = {}
        for v in voters:
            party = v.party_affiliation.strip()
            if party in parties:
                parties[party] += 1
            else:
                parties[party] = 1

        labels = list(parties.keys())
        values = list(parties.values())

        fig = go.Pie(labels=labels, values=values)
        graph_div_parties = plotly.offline.plot(
            {
                "data": [fig],
                "layout_title_text": "Distribution of Voters by Party Affiliation",
            },
            auto_open=False,
            output_type="div",
        )
        context["graph_div_parties"] = graph_div_parties

        # graph 3: bar chart of election participation
        x = ["v20state", "v21town", "v21primary", "v22general", "v23town"]
        y = [
            voters.filter(v20state=True).count(),
            voters.filter(v21town=True).count(),
            voters.filter(v21primary=True).count(),
            voters.filter(v22general=True).count(),
            voters.filter(v23town=True).count(),
        ]

        fig = go.Bar(x=x, y=y)
        graph_div_elections = plotly.offline.plot(
            {"data": [fig], "layout_title_text": "Participation in Elections"},
            auto_open=False,
            output_type="div",
        )
        context["graph_div_elections"] = graph_div_elections

        return context
